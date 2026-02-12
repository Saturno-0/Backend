from pydantic import BaseModel, ConfigDict


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserMeResponse(BaseModel):
    id: int
    username: str
    role: str
    parroquia_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
