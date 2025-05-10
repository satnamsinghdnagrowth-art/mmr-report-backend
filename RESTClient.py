# main.py
from server.init import app
from helper.LoadJsonData import load_section_configs
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    load_section_configs()


def runServer():
    try:
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as ex:
        print(f"Error: {ex}")
