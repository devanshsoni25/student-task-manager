from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from core.database import CollectionUser,mongodb_client
from core.security import hash_password,verify_password
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

app=FastAPI()

class UserRegistration(BaseModel):
    name:str
    email:EmailStr
    password:str
    confirm_password:str

class UserLogin(BaseModel):
    email : EmailStr
    password : str


@app.post("/register")
async def register_user(user:UserRegistration):

    email = user.email.lower()

    if len(user.password)<8:
        raise HTTPException(status_code = 400, detail= "Password must be at least 8 characters")

    if user.password!=user.confirm_password:
        raise HTTPException(status_code= 400 , detail= "Password does not match")
    
    existing_user=await CollectionUser.find_one({
        "email":email
    })

    if existing_user:
        raise HTTPException(status_code= 409 , detail= "Email already registered")
    

    
    try: await CollectionUser.insert_one({
        "name":user.name,
        "email":email,
        "password":hash_password(user.password)
    })
    except DuplicateKeyError:
        raise HTTPException(status_code= 409, detail= "Email alreday registered")

    return{
        "message":"user registration is sucessful"
    }

@app.post("/login")
async def login_user(user: UserLogin):
    email = user.email.lower()

    existing_user = await CollectionUser.find_one({
        "email": email

    })
    if not existing_user:
        raise HTTPException(status_code=401,detail="Invalid email or password ")

    if not verify_password(user.password,existing_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "Login successful"
    }
