# from fastapi import FastAPI, HTTPException, Path, status
# from pydantic import BaseModel
# from typing import Optional
#
# app = FastAPI()
# class User(BaseModel):
#     name:str
#     password:str
#     email:str
# #
#
# class UpdateUser(BaseModel):
#     name: Optional[str] = None
#     password: Optional[str] = None
#     email: Optional[str] = None
#
# users = {
#     101: {'name': 'John', 'password': '<PASSWORD>', 'email': '<EMAIL>'},
# }
#
# #Get users
# @app.get('/users/{user_id}')
# async def get_user(user_id: int):
#     if user_id not in users:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')
#     else:
#         return users[user_id]
# # add a user
# @app.post('/users')
# async def create_user(id:int, name:str,password:str,email:str):
#
#     users[id] = {'name':name, 'password':password, 'email':email}
#     return users[id]
# @app.put('/users/{user_id}')
# async def update_user(user_id:int, name:str,password:str,email:str):
#     if user_id not in users:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')
#     if name in users[user_id]['name']:
#
# @app.delete('/users/{user_id}')
# async def delete_user(user_id:int):
#     if user_id not in users:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')
#     else:
#         del users[user_id]
#         return {'message': 'User deleted'}
#
#
#
# items = []
#
#
#
#
#
# @app.get("/add/{num1}/{num2}", name="add")
# def root(num1: int, num2: int):
#     return {"result": num1 + num2}
#
# @app.post("/items")
# def create_item(item:str):
#     items.append(item)
#     return items
#
# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     try:
#         return items[item_id]
#     except IndexError:
#         raise HTTPException(status_code=404, detail="Item not found")