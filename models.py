from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,Text
from typing import List


class Base(DeclarativeBase):
    pass



class UserModel(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)
    comments:Mapped[List["CommentModel"]] = relationship(back_populates='user')

class CommentModel(Base):
    __tablename__ = 'comments'
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    text:Mapped[str] = mapped_column(Text,nullable=False)
    user:Mapped["UserModel"] =relationship(back_populates='comments')

