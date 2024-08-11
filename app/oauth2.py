from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# SECRET_KEY
# Algorithm
# Exprition time of the token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

  
def create_access_token(data: dict):
    to_encode = data.copy()
     
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt =jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Ensure the id is fetched as a string
        id: str = str(payload.get("user_id"))
        
        if id is None:
            raise credentials_exception
        
        # Pass the id as a string to TokenData
        token_data = schema.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data

    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate the credentials", 
                                           headers={'WWW-Authenticate': "Bearer"})
    token = verify_access_token(token, credentials_exceptions)

    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user