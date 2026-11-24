from fastapi import FastAPI
from app.api.routes.runs import router as runs_router

app = FastAPI()

app.include_router(runs_router)