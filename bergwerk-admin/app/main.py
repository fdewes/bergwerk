import os
import requests
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from pydantic import BaseModel
from passlib.context import CryptContext
from redis_config import get_all_config, update_config
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Depends, FastAPI, Request, Form, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

class RootPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        prefix = request.headers.get("x-forwarded-prefix")
        if prefix:
            request.scope["root_path"] = prefix
        response = await call_next(request)
        return response
    
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.add_middleware(RootPathMiddleware)
templates = Jinja2Templates(directory="templates")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    form_data = OAuth2PasswordRequestForm(
        username=username,
        password=password,
        scope="",
        client_id=None,
        client_secret=None,
    )
    try:
        token = await login_for_access_token(form_data)

        response = RedirectResponse(url=request.scope.get("root_path", "") + "/", status_code=302)
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,         # Important for security
            max_age=1800,          # 30 minutes
            path="/",
            secure=False,          # Set to True if using HTTPS
            samesite="lax",
        )
        return response

    except HTTPException as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": e.detail})



@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/admin/login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(fake_users_db, username)
        if not user or user.disabled:
            raise HTTPException(status_code=401, detail="Invalid user")
    except InvalidTokenError:
        return RedirectResponse("/admin/login")

    config = get_all_config()
    return templates.TemplateResponse("index.html", {"request": request, "config": config, "user": user})


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/admin/login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(fake_users_db, username)
        if not user or user.disabled:
            raise HTTPException(status_code=401, detail="Invalid user")
    except InvalidTokenError:
        return RedirectResponse("/admin/login")
    
    content = await file.read()
    files = {'file': (file.filename, content, 'multipart/form-data')}
    response = requests.post("http://api/admin/import/", files=files)
    return JSONResponse({"filename": file.filename, "size": len(content)})

@app.get("/trigger/build")
async def build_intent_classifier(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/admin/login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(fake_users_db, username)
        if not user or user.disabled:
            raise HTTPException(status_code=401, detail="Invalid user")
    except InvalidTokenError:
        return RedirectResponse("/login")
    
    response = requests.get("http://api/admin/build_intent_classifier/")
    return JSONResponse({"message": response.text})

@app.get("/trigger/export")
async def trigger_export(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/admin/login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(fake_users_db, username)
        if not user or user.disabled:
            raise HTTPException(status_code=401, detail="Invalid user")
    except InvalidTokenError:
        return RedirectResponse("/login")
    
    response = requests.get("http://api/admin/export/")
    with open("export.json", "wb") as f:
        f.write(response.content)
    return FileResponse("export.json", filename="export.json", media_type='application/json')

@app.get("/trigger/generate")
async def trigger_generate(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/admin/login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(fake_users_db, username)
        if not user or user.disabled:
            raise HTTPException(status_code=401, detail="Invalid user")
    except InvalidTokenError:
        return RedirectResponse("/admin/login")

    response = requests.get("http://api/llm/llm_training_data/")
    return JSONResponse({"message": response.text})

@app.post("/config/update")
async def config_update(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/admin/login")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(fake_users_db, username)
        if not user or user.disabled:
            raise HTTPException(status_code=401, detail="Invalid user")
    except InvalidTokenError:
        return RedirectResponse("/admin/login")

    form = await request.form()
    update_config(dict(form))
    return RedirectResponse(request.scope.get("root_path") + "/", status_code=302)

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
