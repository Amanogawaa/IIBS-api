from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.database import engine
import api.models as models
from api.views import Routes

def create_app() -> FastAPI:
    app = FastAPI()

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    
    origins = [
    "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(Routes, prefix="/api")

    models.Base.metadata.create_all(bind=engine)

    print("Server is running...")

    return app


app = create_app()
