from datetime import datetime
from core.models.base.ResultModel import  Result
from database.dbConnection import get_connection

def userCreation():
    try:

        db = get_connection()

    except Exception as ex:
        message = f"Error occurred in userCreation: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)