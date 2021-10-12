from fastapi import FastAPI
from cron import daily_update_cron
from routes.counterparty import router as CounterpartyRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to root"}


app.include_router(CounterpartyRouter, tags=["Counterparty"], prefix="/counterparty")

scheduler = AsyncIOScheduler()
scheduler.add_job(
    daily_update_cron,
    CronTrigger(hour='6')   #trigger 6am everyday.
)
scheduler.start()