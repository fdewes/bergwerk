import os
from fastapi import Request, HTTPException

def check_auth(request: Request):
    username = request.cookies.get("user")
    password = request.cookies.get("pass")
    if username != os.getenv("MEDIAWIKI_ADMIN") or password != os.getenv("MEDIAWIKI_ADMIN_PASSWORD"):
        #raise HTTPException(status_code=401, detail="Unauthorized")
        pass
