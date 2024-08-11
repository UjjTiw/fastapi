from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, models, utils, schema, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schema.Token)
# def login(user_creds: schema.UserCreds, db:Session = Depends(database.get_db)):
def login(user_creds: OAuth2PasswordRequestForm= Depends(), db:Session = Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_creds(user_creds.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    #create token
    # return token
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {'access_token': access_token, "token_type": "bearer"} 