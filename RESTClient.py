# main.py
from server.init import app
from helper.LoadJsonData import load_section_configs
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from helper.InitalFolderCreation import create_required_folders

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler for Validatio Errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "Status": 0,
            "Message": "Invalid request format or data type",
            "Errors": exc.errors(),
            "RequestBody": await request.json()
            if request.method in ("POST", "PUT", "PATCH")
            else None,
        },
    )


@app.on_event("startup")
def startup_event():
    load_section_configs()
    create_required_folders()


def runServer():
    try:
        uvicorn.run(app, host="0.0.0.0", port=8081)
    except Exception as ex:
        print(f"Error: {ex}")
