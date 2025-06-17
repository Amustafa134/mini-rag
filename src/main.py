
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")

from routes import base

app = FastAPI()

#@app.get("/")
#def welcome():
#   return {
#        "message": "Hello World!"
#    }

app.include_router(base.base_router)