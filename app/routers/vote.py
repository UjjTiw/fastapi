from fastapi import FastAPI, Response, HTTPException, Depends, status, APIRouter
from .. import oauth2, schema, models, utils, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/')
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Correctly construct the query to check if the vote already exists
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    vote_cond = vote_query.first()

    if vote.dir == 1:
        if vote_cond:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} has already voted on this post")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not vote_cond:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
