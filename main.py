from fastapi import FastAPI
from routes.demo import router as DemoRouter


app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to root"}


app.include_router(DemoRouter, tags=["Demo"], prefix="/demo")