from datetime import datetime, timezone


class MemoryConfidence:

    SIMILARITY_WEIGHT = 0.40
    IMPORTANCE_WEIGHT = 0.25
    ACCESS_WEIGHT = 0.20
    RECENCY_WEIGHT = 0.15

    @staticmethod
    def calculate(
        memory: dict,
    ) -> float:

        similarity = float(
            memory.get(
                "score",
                0.0,
            )
        )

        importance = int(
            memory.get(
                "importance",
                1,
            )
        )

        access_count = int(
            memory.get(
                "access_count",
                0,
            )
        )

        last_accessed = memory.get(
            "last_accessed",
        )

        # -----------------------------
        # Importance
        # -----------------------------

        importance_score = min(
            importance / 10,
            1.0,
        )

        # -----------------------------
        # Access Count
        # -----------------------------

        access_score = min(
            access_count / 20,
            1.0,
        )

        # -----------------------------
        # Recency
        # -----------------------------

        recency_score = 0.5

        if last_accessed:

            try:

                if isinstance(
                    last_accessed,
                    str,
                ):

                    dt = datetime.fromisoformat(
                        last_accessed.replace(
                            "Z",
                            "+00:00",
                        )
                    )

                else:

                    dt = last_accessed

                if dt.tzinfo is None:
                    dt = dt.replace(
                        tzinfo=timezone.utc,
                    )

                now = datetime.now(
                    timezone.utc,
                )

                days = (
                    now - dt
                ).days

                recency_score = max(
                    0.0,
                    1 - (days / 30),
                )

            except Exception:

                recency_score = 0.5

        # -----------------------------
        # Final Confidence
        # -----------------------------

        confidence = (
            similarity
            * MemoryConfidence.SIMILARITY_WEIGHT
            + importance_score
            * MemoryConfidence.IMPORTANCE_WEIGHT
            + access_score
            * MemoryConfidence.ACCESS_WEIGHT
            + recency_score
            * MemoryConfidence.RECENCY_WEIGHT
        )

        return round(
            min(
                confidence,
                1.0,
            ),
            3,
        )