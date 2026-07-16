class MemoryRanker:

    # Weight Configuration
    IMPORTANCE_WEIGHT = 0.50
    SIMILARITY_WEIGHT = 0.30
    RECENCY_WEIGHT = 0.20

    @staticmethod
    def rank(
        memories: list,
    ) -> list:
        """
        Rank memories using:
        - Importance
        - Vector Similarity
        - Recency (optional for now)

        Final Score =
            importance * 0.5
          + similarity * 10 * 0.3
          + recency * 0.2
        """

        if not memories:
            return []

        ranked = []

        for memory in memories:

            importance = memory.get(
                "importance",
                1,
            )

            similarity = memory.get(
                "score",
                0.0,
            )

            # Placeholder
            # Later we'll calculate from created_at
            recency = memory.get(
                "recency",
                0,
            )

            final_score = (
                (importance * MemoryRanker.IMPORTANCE_WEIGHT)
                + (
                    (similarity * 10)
                    * MemoryRanker.SIMILARITY_WEIGHT
                )
                + (
                    recency
                    * MemoryRanker.RECENCY_WEIGHT
                )
            )

            memory["final_score"] = round(
                final_score,
                2,
            )

            ranked.append(memory)

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True,
        )

        return ranked