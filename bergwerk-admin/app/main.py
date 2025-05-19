from typing import Annotated
from pydantic import BaseModel
from passlib.context import CryptContext


from fastapi import Depends, FastAPI, Request, Form, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from redis_config import get_all_config, update_config
from auth import check_auth
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os
import requests

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class RootPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        prefix = request.headers.get("x-forwarded-prefix")
        if prefix:
            request.scope["root_path"] = prefix
        response = await call_next(request)
        return response
    
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI() 
app.add_middleware(RootPathMiddleware)

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    check_auth(request)
    config = get_all_config()
    return templates.TemplateResponse("index.html", {"request": request, "config": config})

@app.post("/login")
async def login(request: Request, user: str = Form(...), password: str = Form(...)):
    if user == os.getenv("MEDIAWIKI_ADMIN") and password == os.getenv("MEDIAWIKI_ADMIN_PASSWORD"):
        response = RedirectResponse(request.scope.get("root_path") + "/", status_code=302)
        response.set_cookie("user", user)
        response.set_cookie("pass", password)
        return response
    return HTMLResponse("Unauthorized", status_code=401)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    files = {'file': (file.filename, content, 'multipart/form-data')}
    response = requests.post("http://api/admin/import/", files=files)
    return JSONResponse({"filename": file.filename, "size": len(content)})

@app.get("/trigger/build")
async def build_intent_classifier():
    response = requests.get("http://api/admin/build_intent_classifier/")
    return JSONResponse({"message": response.text})

@app.get("/trigger/export")
async def trigger_export():
    response = requests.get("http://api/admin/export/")
    with open("export.json", "wb") as f:
        f.write(response.content)
    return FileResponse("export.json", filename="export.json", media_type='application/json')

@app.get("/trigger/generate")
async def trigger_generate():
    response = requests.get("http://api/llm/llm_training_data/")
    return JSONResponse({"message": response.text})

@app.post("/config/update")
async def config_update(request: Request):
    check_auth(request)
    form = await request.form()
    update_config(dict(form))
    return RedirectResponse(request.scope.get("root_path") + "/", status_code=302)

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
