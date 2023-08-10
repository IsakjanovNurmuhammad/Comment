from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from dtbs import Base, engine, get_db
from project_models import Comment, User
from project_schemas import UserSchema, CommentSchema

app = FastAPI()
Base.metadata.create_all(engine)


@app.get('/all_comments')
async def read_comm(db: Session = Depends(get_db)):
    query = db.query(Comment).all()
    return query


@app.get('/all_users')
async def see_users(db: Session = Depends(get_db)):
    query = db.query(User).all()
    return query


@app.post('/register_user')
async def create_user(user: UserSchema,
                      db: Session = Depends(get_db)):
    user_model = User()
    user_model.username = user.username
    user_model.password = user.password
    user_model = user.email

    db.add(user_model)
    db.commit()
    return user_model


@app.post('/add_comment')
async def create_comment(comment: CommentSchema,
                         db: Session = Depends(get_db)):
    comment_model = Comment()
    comment_model.comment = comment.comment

    db.add(comment_model)
    db.commit()
    return comment_model


@app.put("/update/user")
async def edit_user(Userid: int,
                    schema: UserSchema,
                    db: Session = Depends(get_db)):
    model = db.query(User).filter(User.id == Userid).first()

    if model is None:
        return "Is none"
    else:
        model_ = User()
        model_.email = schema.email
        model_.password = schema.password
        model_.username = schema.username

        db.add(model_)
        db.commit()

        return model_


@app.put("/update/comment")
async def edit_comment(commentid: int,
                    schema: CommentSchema,
                    db: Session = Depends(get_db)):
    model = db.query(Comment).filter(Comment.id == commentid).first()

    if model is None:
        return "Is none"
    else:
        comment_model = Comment()
        comment_model.comment = schema.comment

        db.add(comment_model)
        db.commit()
        return comment_model


@app.delete("/delete-user")
async def del_user(user_id: int,
                   db: Session = Depends(get_db)):
    query = db.query(User).filter(User.id == user_id).first()
    if query is None:
        return f"No user with ID {id}"
    else:
        db.delete(query)
        db.commit()
        return "Successfully deleted"


@app.delete("/delete-comment")
async def del_comment(comment_id: int,
                   db: Session = Depends(get_db)):
    query = db.query(Comment).filter(Comment.id == comment_id).first()
    if query is None:
        return f"No comment with ID {id}"
    else:
        db.delete(query)
        db.commit()
        return "Successfully deleted"
