from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis_config import init_defaults, get_all_config, update_config
from auth import check_auth
import os
import requests


from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI
import os

class RootPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        prefix = request.headers.get("x-forwarded-prefix")
        if prefix:
            request.scope["root_path"] = prefix
        response = await call_next(request)
        return response

app = FastAPI()  # Important for Caddy proxy path handling
app.add_middleware(RootPathMiddleware)

templates = Jinja2Templates(directory="templates")

init_defaults()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        check_auth(request)
        config = get_all_config()
        return templates.TemplateResponse("index.html", {"request": request, "config": config})
    except:
        return templates.TemplateResponse("login.html", {"request": request})

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
