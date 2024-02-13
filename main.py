from fastapi import FastAPI, Request
from routers import battle

app = FastAPI()

app.include_router(battle.router)

@app.get("/")
async def root():
    obj = Request.get()
    return {"message": "Hello World"}