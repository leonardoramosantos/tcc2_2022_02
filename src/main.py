from typing import Union

from fastapi import FastAPI

from .actions.routes import router as actions_router
from .internal.routes import router as internal_router

app = FastAPI()

app.include_router(actions_router, prefix="/actions")
app.include_router(internal_router, prefix="/internal")

@app.get("/")
def read_root():
    return {"Hello": "World"}