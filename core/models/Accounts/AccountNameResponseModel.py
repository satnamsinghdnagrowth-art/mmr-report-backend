from pydantic import BaseModel

class AccountNameModel(BaseModel):
    Name : str
    Code : str