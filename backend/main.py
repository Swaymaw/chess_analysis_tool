import json
import os

from contextlib import asynccontextmanager
from src.utils.types import EngineTypes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.utils.helper import get_engine

from src.routes.v1_router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load env before anything else
    load_dotenv(override=True)

    # --- STARTUP ---
    print("🚀 Initializing Chess Engines and AI Client...")

    get_engine(EngineTypes.STOCKFISH)

    yield

    # --- SHUTDOWN ---
    print("🛑 Shutting down engines...")
    for engine in app.state.engines.values():
        engine.quit()

    print("Cleanup complete.")


app = FastAPI(title="Chess API", lifespan=lifespan)
app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=json.loads(os.getenv("CORS_ORIGINS", "[]")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    return {"status": "running"}
