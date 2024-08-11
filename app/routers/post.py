from .. import models, schema, utils, oauth2
from fastapi import FastAPI, Response, HTTPException, Depends, status, APIRouter
from ..database import engine, get_db 
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=['Users']
)

#retreieving data use the get http request 
@router.get('/',response_model=List[schema.PostWithVotes]) #@app.get('/') fast api looks for the first match so if samer rahgea toh upar weawla chalega re
async def get_posts(db: Session = Depends(get_db), curr_user:int= Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # my_posts = cursor.fetchall()
    my_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()# in search option for space purpose use "%" for it
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get('/users/{owner_id}', response_model=List[schema.Post])
async def get_posts(owner_id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    # Ensure that the requesting user has access to the posts they are trying to fetch
    if owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access these posts")
    
    # Fetch posts for the given owner_id
    my_posts = db.query(models.Post).filter(models.Post.owner_id == owner_id).all()
    
    return my_posts


# postman is used for testing the http request
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post) #here we are changing the http request id since for creating a new id we should always denote it by 201
def create_post(payload: schema.PostCreate, db: Session = Depends(get_db), curr_user:int= Depends(oauth2.get_current_user)):
    # print(payload)
    # print(payload.dict())
    # payload=payload.dict()
    # payload['id'] = randrange(0,2000000000)
    # # return {'message': "successfully created the post"}
    # # return {'new_post': f" title {payload['title']} content: {payload['content']}"}
    # my_posts.append(payload)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payload.title, payload.content, payload.published))
    # new_payload = cursor.fetchone() #didnt commited the chage thats why fucked up so you have to commit it
    # conn.commit()
    print(curr_user.email)
    print(payload.dict())
    new_payload=models.Post(owner_id=curr_user.id,**payload.dict())
    db.add(new_payload)
    db.commit()
    db.refresh(new_payload)
    return  new_payload

# @app.get('posts/latest')
# def get_latest_post():
#     return {'post_detail': my_posts[-1]}
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_with_votes = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    
    if post_with_votes:
        return post_with_votes
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")


# @router.get('/{id}', status_code=status.HTTP_404_NOT_FOUND, response_model=schema.Post) # her e id represents the path parameter also it's in string tht's why converted into integer 
# def get_post(id:int, db: Session = Depends(get_db), curr_user:int= Depends(oauth2.get_current_user)):
#     # cursor.execute(f"""SELECT * FROM  posts WHERE id={id}""")
#     # post = find_post(id)
#     # post = cursor.fetchone()
    
#     post= db.query(models.Post).filter(models.Post.id==id).first()
#     if post:
#         return post
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)# response_model=Post)
def delete_post(id:int, db:Session=Depends(get_db), curr_user:int= Depends(oauth2.get_current_user)):
    # cursor.execute(f"""DELETE FROM posts WHERE id={id} RETURNING *""")
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_post_index(id)
    # if index==None:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()  # Corrected: Now calling `first()` method properly
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#following snipppet gives errort cuz matching the path operationnso move it sup
# @app.get('posts/latest')
# def get_latest_post():
#     return {'post_detail': my_posts[-1]}
 
@router.put('/{id}')
def update_post(id: int, post: schema.PostCreate, db:Session=Depends(get_db), curr_user:int= Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;", (post.title, post.content, post.published, id))

    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post is None:
    #     raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                          detail=f"post with id: {id} does not exist")
    # index = find_post_index(id)
    # if index==None: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # post = post.dict()
    # post['id']= id
    # my_posts[index] = post
    
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    new_post = updated_post.first()
    
    if new_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if new_post.owner_id != curr_user.id:  # Corrected: Use `new_post` instead of `post`
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return {'message': 'successful'}