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

#  practice code
#
# class ModelsName(str, Enum):
#     accepted = 'accepted'
#     pending = 'pending'
#     rejected = 'rejected'
#
# class BodyModel(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: float = None
#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
# # body parameters
# @app.post('/create/')
# async def create_items(item: BodyModel):
#     return item
#
# @app.post('/create/{item_id}')
# async def create_items(item_id: int, item: BodyModel):
#     return {"item_id": item_id, **item.dict()}
#
# # body + query parameters
# @app.get('/item/')
# async def get(q: Union[str, None] = None):
#     result = {"items": fake_items_db}
#
#     if q:
#         result.update({'q': q})
#
#     return result
#
#
# # path parameters
# @app.get('/users/me')
# async def read_user_me():
#     return {"Current User": "ME"}
#
# @app.get('/users/{id}')
# async def read_user(id: int):
#     return {"User" : {"id": id}}
#
# @app.get('/models/{model_name}')
# async def get_model(model_name: ModelsName):
#     if model_name is ModelsName.accepted:
#         return {"model name" : model_name, "message": "This model is accepted"}
#
#     if model_name is ModelsName.pending:
#         return {"model name": model_name, "message": "This model is pending"}
#
#     if model_name.value == 'rejected':
#         return {"model name": model_name, "message": "This model is rejected"}
#
#     return {'model name': model_name, 'message': 'This model is not accepted'}
#
# # query parameters
# @app.get('/items/')
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]
