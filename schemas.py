from pydantic import BaseModel
import datetime
from fastapi import Body

class UserSchema(BaseModel):
    name: str

class CommentSchema(BaseModel):
    body: str