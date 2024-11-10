
from fastapi import FastAPI, Body, HTTPException, Path, Request

import uvicorn
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")
users: List['User'] = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {'request': request, 'user': users})


@app.get('/user/{user_id}')
async def get_get(request: Request, user_id: int) -> HTMLResponse:
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.post('/user/{username}/{age}', response_model=User)
async def add_user(
        username: Annotated[str, Path(description="Имя пользователя")],
        age: Annotated[int, Path(description="Возраст пользователя")]) -> User:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def get_put(user_id: int, username: str, age: int) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        user.username = username
        user.age = age
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def get_del(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]):
    if user_id >= len(users) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        del_user = users.pop(user_id)
        return del_user

