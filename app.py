from fastapi import FastAPI
from main import linkedIn_automate


app = FastAPI()


@app.get("/health")
async def health():
    return {"message": "Server is running"}

@app.get('/call_automate')
async def call_automate():
    linkedIn_automate()