from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .actions.routes import router as actions_router
from .internal.routes import router as internal_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actions_router, prefix="/actions")
app.include_router(internal_router, prefix="/internal")

@app.get("/")
def read_root():
    return {"Hello": "World"}