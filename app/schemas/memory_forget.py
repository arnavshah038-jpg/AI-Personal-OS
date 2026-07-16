from pydantic import BaseModel


class MemoryForgetDecision(BaseModel):
    action: str
    memory: str | None = None

    @classmethod
    def parse(cls, response: str):

        response = response.strip()

        if response == "NO":
            return cls(
                action="NO",
            )

        if response.startswith("YES:"):

            return cls(
                action="YES",
                memory=response.replace(
                    "YES:",
                    "",
                ).strip(),
            )

        return cls(
            action="NO",
        )