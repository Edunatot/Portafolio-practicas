import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from routers.rh import rh

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="."), name="static")

app.include_router(rh.router)

@app.get("/")
def home():
    return FileResponse(Path("index.html"))
