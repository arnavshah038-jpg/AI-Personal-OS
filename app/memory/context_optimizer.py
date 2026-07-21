from app.utils.logger import logger


class ContextOptimizer:

    MAX_LINES = 20
    MAX_CHARACTERS = 4000

    @staticmethod
    def optimize(
        context: str,
    ) -> str:

        if not context:
            return ""

        seen = set()
        optimized = []

        current_size = 0

        for line in context.splitlines():

            line = line.strip()

            if not line:
                continue

            if line in seen:
                continue

            if (
                current_size + len(line)
                > ContextOptimizer.MAX_CHARACTERS
            ):
                break

            seen.add(line)

            optimized.append(line)

            current_size += len(line)

        optimized = optimized[
            :ContextOptimizer.MAX_LINES
        ]

        optimized_context = "\n".join(
            optimized
        )

        logger.info(
            f"[ContextOptimizer] "
            f"Lines={len(optimized)} | "
            f"Characters={len(optimized_context)}"
        )

        return optimized_context