import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web import wiki, admin

app = FastAPI(docs_url=None, redoc_url=None)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["X-Requested-With", "Content-Type"],
)

app.include_router(wiki.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload="True")
