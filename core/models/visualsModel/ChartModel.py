from pydantic import BaseModel


class CartModel(BaseModel):
    Title : str
    Content : str



