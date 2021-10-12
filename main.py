from fastapi import FastAPI
from routes.demo import router as DemoRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to root"}


app.include_router(DemoRouter, tags=["Demo"], prefix="/demo")

scheduler = AsyncIOScheduler()
scheduler.add_job(
    lambda : print("TODO cron job"),
    CronTrigger(hour='6')   #trigger 6am everyday.
)
scheduler.start()