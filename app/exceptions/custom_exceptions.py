class AIServiceError(Exception):
    """Raised when AI service fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)