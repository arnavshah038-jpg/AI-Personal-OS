from app.memory.chat_memory import ChatMemory
from app.memory.summary import ConversationSummary
from app.utils.logger import logger


class MemoryManager:

    @staticmethod
    def summarize_if_needed(session_id: str):

        if not ChatMemory.should_summarize(session_id):
            return

        logger.info(
            f"Summarizing conversation | Session={session_id}"
        )

        history = ChatMemory.build_openai_history(session_id)

        summary = ConversationSummary.summarize(history)

        logger.info(
            f"Conversation Summary:\n{summary}"
        )