from datetime import datetime


class MemoryRanker:

    IMPORTANCE_WEIGHT = 0.45
    SIMILARITY_WEIGHT = 0.35
    RECENCY_WEIGHT = 0.15
    ACCESS_WEIGHT = 0.05


    @staticmethod
    def calculate_recency(memory):

        created_at = memory.get(
            "created_at"
        )

        if not created_at:
            return 0


        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(
                created_at
            )


        days_old = (
            datetime.utcnow()
            - created_at
        ).days


        if days_old <= 1:
            return 1

        elif days_old <= 7:
            return 0.7

        elif days_old <= 30:
            return 0.4

        else:
            return 0.1



    @staticmethod
    def calculate_access(memory):

        count = memory.get(
            "access_count",
            0
        )


        if count >= 10:
            return 1

        elif count >= 5:
            return 0.7

        elif count >= 1:
            return 0.4

        return 0



    @staticmethod
    def rank(
        memories:list
    ):

        if not memories:
            return []


        ranked=[]


        for memory in memories:


            importance = (
                memory.get(
                    "importance",
                    1
                )
                /10
            )


            similarity = memory.get(
                "score",
                0
            )


            recency = (
                MemoryRanker.calculate_recency(
                    memory
                )
            )


            access = (
                MemoryRanker.calculate_access(
                    memory
                )
            )


            final_score = (

                importance
                *
                MemoryRanker.IMPORTANCE_WEIGHT

                +

                similarity
                *
                MemoryRanker.SIMILARITY_WEIGHT

                +

                recency
                *
                MemoryRanker.RECENCY_WEIGHT

                +

                access
                *
                MemoryRanker.ACCESS_WEIGHT

            )


            memory["final_score"] = round(
                final_score,
                3
            )


            ranked.append(
                memory
            )


        ranked.sort(
            key=lambda x:x["final_score"],
            reverse=True
        )


        return ranked