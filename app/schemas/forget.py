from pydantic import BaseModel


class ForgetRequest(BaseModel):
    session_id: str
    message: str


class ForgetResponse(BaseModel):
    message: str