class ContextOptimizer:

    @staticmethod
    def optimize(
        context: str,
    ) -> str:

        if not context:
            return ""

        seen = set()
        optimized = []

        for line in context.splitlines():

            line = line.strip()

            # Remove empty lines
            if not line:
                continue

            # Remove duplicate lines
            if line in seen:
                continue

            seen.add(line)
            optimized.append(line)

        return "\n".join(optimized)