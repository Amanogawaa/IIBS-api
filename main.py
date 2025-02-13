from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from api.database import engine
import api.models as models
from api.views import Routes

# practice code imports
from enum import Enum
from typing import Union
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(Routes, prefix='/api')

models.Base.metadata.create_all(bind=engine)

print('Server is running...')
