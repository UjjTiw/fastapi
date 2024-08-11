from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import utils
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

import time 
from sqlalchemy.orm import Session 
from . import models
from .database import engine, get_db
from .schema import Post, UserCreate, UserResponse
from .routers import post, users, auth,  vote

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
# # always matches the first path opertrations order does matter 
@app.get('/') # path operations 
async def root():
    return {'message': 'hello world'}

# # @app.get('/sqlalchemy')
# # def test_posts(db: Session = Depends(get_db)):
# #     # post=db.query(models.Post).all() selecting al the rows in the database schemea tabel;
# #     return {'status': 'success'}    

# #retreieving data use the get http request 
# @app.get('/posts',response_model=List[Post]) #@app.get('/') fast api looks for the first match so if samer rahgea toh upar weawla chalega re
# async def get_posts(db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts""")
#     # my_posts = cursor.fetchall()
#     my_posts = db.query(models.Post).all()
#     return my_posts

# # postman is used for testing the http request
# @app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post) #here we are changing the http request id since for creating a new id we should always denote it by 201
# def create_post(payload: Post, db: Session = Depends(get_db)):
#     # print(payload)
#     # print(payload.dict())
#     # payload=payload.dict()
#     # payload['id'] = randrange(0,2000000000)
#     # # return {'message': "successfully created the post"}
#     # # return {'new_post': f" title {payload['title']} content: {payload['content']}"}
#     # my_posts.append(payload)
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payload.title, payload.content, payload.published))
#     # new_payload = cursor.fetchone() #didnt commited the chage thats why fucked up so you have to commit it
#     # conn.commit()
#     new_payload=models.Post(title=payload.title, content=payload.content, published=payload.published)

#     db.add(new_payload)
#     db.commit()
#     db.refresh(new_payload)
#     return  new_payload

# # @app.get('posts/latest')
# # def get_latest_post():
# #     return {'post_detail': my_posts[-1]}

# @app.get('/posts/{id}', status_code=status.HTTP_404_NOT_FOUND, response_model=Post) # her e id represents the path parameter also it's in string tht's why converted into integer 
# def get_post(id:int, db: Session = Depends(get_db)):
#     # cursor.execute(f"""SELECT * FROM  posts WHERE id={id}""")
#     # post = find_post(id)
#     # post = cursor.fetchone()
#     post= db.query(models.Post).filter(models.Post.id==id).first()
#     if post:
#         return post
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)# response_model=Post)
# def delete_post(id:int, db:Session=Depends(get_db) ):
#     # cursor.execute(f"""DELETE FROM posts WHERE id={id} RETURNING *""")
#     # deleted_post = cursor.fetchone()
#     # conn.commit()
#     # index = find_post_index(id)
#     # if index==None:
#     post_query=db.query(models.Post).filter(models.Post.id==id)

#     if post_query.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     post_query.delete(synchronize_session=False)
#     db.commit()
#     # print(index)
#     # my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # return {'deleted_post': deleted_post}


# #following snipppet gives errort cuz matching the path operationnso move it sup
# # @app.get('posts/latest')
# # def get_latest_post():
# #     return {'post_detail': my_posts[-1]}
 
# @app.put('/posts/{id}')
# def update_post(id: int, post: Post, db:Session=Depends(get_db)):
#     # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", (post.title, post.content, post.published, id))

#     # updated_post = cursor.fetchone()
#     # conn.commit()
#     # if updated_post is None:
#     #     raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                          detail=f"post with id: {id} does not exist")
#     # index = find_post_index(id)
#     # if index==None: 
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     # post = post.dict()
#     # post['id']= id
#     # my_posts[index] = post
    
#     updated_post=db.query(models.Post).filter(models.Post.id==id)
#     new_post = updated_post.first()
#     if new_post is None:
#         raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"post with id: {id} does not exist")
#     updated_post.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return {'message': 'succesful'}


# @app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     user.password = utils.hash(user.password)
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user) 
#     return new_user

# @app.get('/users/{id}', response_model=UserResponse)
# def get_user(id:int, db: Session = Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exists")

#     return user