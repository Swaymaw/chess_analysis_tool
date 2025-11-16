from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.v1_router import api_v1_router

app = FastAPI(title="Chess API")
app.include_router(api_v1_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bishup.com", "https://www.bishup.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    return {"status": "running"}
