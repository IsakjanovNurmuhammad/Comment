from pydantic import BaseModel


class CommentSchema(BaseModel):
    comment: str


class UserSchema(BaseModel):
    username: str
    password: str
    email: str
