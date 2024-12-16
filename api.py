from fastapi import FastAPI, HTTPException
import uvicorn
from models import *
from config import *
from response_models import*

app = FastAPI(
    title = "yourtitle",
    description = "pracrAPI",
    version = "1.0.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

@app.get("/users/select/{user_id}")
async def get_users(user_id:int):
    try:
        with DBSettings.get_session() as conn:
            user = conn.query(User).filter(User.id==user_id).first()
            return user
    except:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/add", response_model= UserCreate)
async def add_users(user_name:str, user_role:str): 
    user = UserCreate(name=user_name, role = user_role)
    with DBSettings.get_session() as conn:
        roleDB = conn.query(Role).filter(Role.name == user.role).first()
        if (roleDB == None):
            raise HTTPException(status_code=404, detail="We haven't this role")
        else:
            new_user = User(name = user.name, role_id = roleDB.id)
            conn.add(new_user)
            conn.commit()
            return user

@app.put("/users/update/{user_id}", response_model=UserCreate)
async def update_user(user_id: int, user_name: str, user_role: str):
    try:
        with DBSettings.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
  
            user.name = user_name
            roleDB = conn.query(Role).filter(Role.name == user_role).first()
            if roleDB is None:
                raise HTTPException(status_code=404, detail="We haven't this role")
            else:
                user.role_id = roleDB.id
            conn.commit()
            return UserCreate(name=user.name, role=user_role)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    try:
        with DBSettings.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            conn.delete(user) 
            conn.commit()  
            return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


uvicorn.run(app, host="127.0.0.1", port = 8000)