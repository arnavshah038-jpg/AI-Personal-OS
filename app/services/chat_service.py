from fastapi import Request
from openai import OpenAIError

from app.core.config import settings
from app.core.openai_client import client
from app.core.prompt_builder import build_memory_prompt
from app.database.session import SessionLocal
from app.exceptions.custom_exceptions import AIServiceError
from app.memory.chat_memory import ChatMemory
from app.memory.memory_consolidator import MemoryConsolidator
from app.memory.memory_decay_manager import MemoryDecayManager
from app.memory.memory_boost_manager import MemoryBoostManager
from app.memory.memory_extractor import MemoryExtractor
from app.memory.memory_forgetter import MemoryForgetter
from app.memory.memory_importance import MemoryImportance
from app.memory.memory_manager import MemoryManager
from app.memory.memory_type_classifier import MemoryTypeClassifier

from app.memory.memory_retriever import MemoryRetriever
from app.memory.vector_store import VectorStore
from app.repositories.memory_repository import MemoryRepository
from app.utils.logger import logger
from app.memory.episode_extractor import EpisodeExtractor
from app.repositories.episode_repository import EpisodeRepository
from app.memory.reflection_manager import ReflectionManager
from app.memory.context_optimizer import ContextOptimizer


def chat(
    request: Request,
    session_id: str,
    message: str,
):
    request_id = request.state.request_id

    try:

        logger.info(f"[{request_id}] User Message: {message}")

        # Save current user message
        ChatMemory.save_message(
            session_id=session_id,
            role="user",
            message=message,
        )

        # --------------------------------------------------
        # FORGET MEMORY
        # --------------------------------------------------

        forget_decision = MemoryForgetter.should_forget(
            message
        )

        logger.info(
            f"FORGET DECISION RESULT: {forget_decision}"
        )

        if forget_decision.action == "YES":

            db = SessionLocal()

            try:

                memory = MemoryRepository.find_memory(
                    db=db,
                    session_id=session_id,
                    memory=forget_decision.memory,
                )

                if memory:

                    MemoryRepository.delete_memory(
                        db=db,
                        session_id=session_id,
                        memory=memory.memory,
                    )

                    VectorStore.delete_memory(
                        memory_id=memory.id,
                    )

                    logger.info(
                        f"Forgot memory: {memory.memory}"
                    )

                    return {
                        "response": "Got it — I’ll forget that memory and won’t use it going forward.",
                        "sources": []
                    }

            finally:

                db.close()

        # --------------------------------------------------
        # Conversation History
        # --------------------------------------------------

        history = ChatMemory.build_openai_history(
            session_id=session_id,
        )

        # --------------------------------------------------
        # Hybrid Memory Retrieval
        # (Semantic + Episode + Reflection - all in one)
        # --------------------------------------------------

        memory_result = MemoryRetriever.retrieve(
            session_id=session_id,
            query=message,
        )

        logger.info(
            f"Memory Sources: {memory_result.get('sources')}"
        )

        memory_context = memory_result["context"]
        memory_sources = memory_result["sources"]

        # --------------------------------------------------
        # Context Optimization
        # --------------------------------------------------

        memory_context = ContextOptimizer.optimize(
            memory_context
        )

        if memory_context:

            memory_prompt = build_memory_prompt(
                memory_context
            )

            history.insert(
                0,
                memory_prompt
            )

        # --------------------------------------------------
        # OpenAI Response
        # --------------------------------------------------

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=history,
        )

        ai_response = response.output_text

        logger.info(
            f"Memory Sources Used: {memory_sources}"
        )

        ChatMemory.save_message(
            session_id=session_id,
            role="assistant",
            message=ai_response,
        )

        # --------------------------------------------------
        # Memory Extraction
        # --------------------------------------------------

        extracted_memory = MemoryExtractor.extract(
            message
        )

        logger.info(
            f"Extracted Memory: {extracted_memory}"
        )

        # --------------------------------------------------
        # Episode Extraction
        # --------------------------------------------------

        episode = EpisodeExtractor.extract(message)

        logger.info(f"Episode Decision: {episode}")

        if episode.action == "SAVE":

            db = SessionLocal()

            try:

                EpisodeRepository.save_episode(
                    db=db,
                    session_id=session_id,
                    title=episode.title,
                    description=episode.description,
                    event_type=episode.event_type,
                )

                logger.info(
                    f"Episode saved: {episode.title}"
                )

            finally:

                db.close()

        # --------------------------------------------------
        # Memory Processing
        # --------------------------------------------------

        if extracted_memory != "NONE":

            db = SessionLocal()

            try:

                existing_memories = (
                    MemoryRepository.get_memory_text(
                        db=db,
                        session_id=session_id,
                    )
                )

                decision = MemoryConsolidator.consolidate(
                    existing_memories=existing_memories,
                    new_memory=extracted_memory,
                )

                logger.info(
                    f"Memory Decision: {decision}"
                )

                # ---------------- KEEP ----------------

                if decision.action == "KEEP":

                    importance = MemoryImportance.score(
                        extracted_memory
                    )

                    memory_type = MemoryTypeClassifier.classify(
                        extracted_memory
                    )

                    saved_memory = (
                        MemoryRepository.save_memory(
                            db=db,
                            session_id=session_id,
                            memory=extracted_memory,
                            importance=importance,
                            memory_type=memory_type,
                        )
                    )

                    VectorStore.save_memory(
                        session_id=session_id,
                        memory_id=saved_memory.id,
                        memory=extracted_memory,
                        memory_type=memory_type,
                        importance=importance,
                    )

                    logger.info(
                        f"New {memory_type} memory saved."
                    )

                # ---------------- IGNORE ----------------

                elif decision.action == "IGNORE":

                    logger.info(
                        "Duplicate memory ignored."
                    )

                # ---------------- UPDATE ----------------

                elif decision.action == "UPDATE":

                    memory = (
                        MemoryRepository.get_memory_by_id(
                            db=db,
                            memory_id=decision.memory_id,
                        )
                    )

                    if memory:

                        importance = MemoryImportance.score(
                            decision.new_memory
                        )

                        memory_type = MemoryTypeClassifier.classify(
                            decision.new_memory
                        )

                        MemoryRepository.update_memory_by_text(
                            db=db,
                            session_id=session_id,
                            old_memory=memory.memory,
                            new_memory=decision.new_memory,
                            importance=importance,
                            memory_type=memory_type,
                        )

                        VectorStore.update_memory(
                            memory_id=memory.id,
                            session_id=session_id,
                            memory=decision.new_memory,
                            memory_type=memory_type,
                            importance=importance,
                        )

                        logger.info(
                            f"{memory_type} memory updated successfully."
                        )

                    else:

                        logger.warning(
                            "Memory ID not found."
                        )

            finally:

                db.close()

            # --------------------------------------------------
            # Reflection Memory
            # (Only runs when a new memory was actually extracted)
            # --------------------------------------------------

            ReflectionManager.generate_if_needed(
                session_id=session_id,
            )

        # --------------------------------------------------
        # Memory Boost
        # --------------------------------------------------

        MemoryBoostManager.run()

        # --------------------------------------------------
        # Conversation Summary
        # --------------------------------------------------

        MemoryManager.summarize_if_needed(
            session_id,
        )

        # --------------------------------------------------
        # Memory Decay
        # --------------------------------------------------

        MemoryDecayManager.run()

        logger.info(
            f"[{request_id}] Response generated successfully."
        )

        return {
            "response": ai_response,
            "sources": memory_result.get(
                "sources",
                []
            )
        }

    except OpenAIError as e:

        logger.error(
            f"[{request_id}] OpenAI Error: {e}"
        )

        raise AIServiceError(
            "AI service is currently unavailable."
        )