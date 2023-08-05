from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from db import Base
from db import engine
from db import session_local
from models import UserModel, CommentModel
from schemas import CommentSchema
from schemas import UserSchema

Base.metadata.create_all(bind=engine)

user_id = 0
comment_id = 0

app = FastAPI()

# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_user(db, id: int):
    return db.query(UserModel).filter(UserModel.id == id).first()
async def get_current_user(db: Session = Depends(get_db)):
    a = db.get("id")
    user = get_user(db,a)
    if user is None:
        return "Not found"
    return user



@app.get("/get-all")
async def get_db_list(db: Session = Depends(get_db)):
    query = db.query(UserModel).all()
    print(get_current_user(db))
    return query


@app.get("/user/{id}")
async def get_user(id: int,
                   db: Session = Depends(get_db)):
    query = db.query(UserModel).filter(UserModel.id == id).first()
    if query is None:
        return "User not found"
    else:
        return query


@app.post("/create/user")
async def create_user(schema: UserSchema,
                      db: Session = Depends(get_db), user_id=user_id):
    model = UserModel()
    model.id = user_id + 1
    user_id += 1
    model.name = schema.name

    db.add(model)
    db.commit()

    return model


@app.put("/update/user")
async def edit_user(id: int,
                    schema: UserSchema,
                    db: Session = Depends(get_db)):

    model = db.query(UserModel).filter(UserModel.name == schema.name).first()

    if model is None:
        return "Is none"
    else:
        model_ = UserModel
        model_.user_id = id
        model_.name = schema.name

        db.add(model_)
        db.commit()

        return model_


@app.delete("/{id}")
async def del_user(id:int,
                   db: Session = Depends(get_db)):
    query = db.query(UserModel).filter(UserModel.user_id == id).first()
    if query is None:
        return f"No user with ID {id}"
    else:
        db.delete(query)
        db.commit()
        return "Successfully deleted"


@app.get("/all-comments")
async def get_all_comments(db: Session = Depends(get_db)):
    query = db.query(CommentModel).all()

    return query


@app.get("/comment/{id}")
async def get_comment(id:int,
                      db: Session = Depends(get_db)):
    query = db.query(CommentModel).filter(CommentModel.id == id).first()
    if query is None:
        return "Comment not found"
    else:
        return query


@app.post("/new-comment")
async def add_comment(schema: CommentSchema,
                      db: Session = Depends(get_db), comment_id=comment_id):
    model = CommentModel()
    model.id = comment_id + 1
    comment_id += 1
    model.body = schema.body

    db.add(model)
    db.commit()


@app.put("edit-comment")
async def edit_comment(id:int,
                       schema: CommentSchema,
                       db: Session = Depends(get_db),
                       ):

    model = db.query(CommentModel).filter(CommentModel.id == id).first()

    if model is None:
        return "Is none"
    else:
        model.id = id
        model.comment = schema.comment

        db.add(model)
        db.commit()

        return model
@app.delete("/del-comment/{id}")
async def del_comment(id: int,
                      db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter_by(id=id).first()
    db.delete(comment)
    db.commit()
    return "Successfully deleted"