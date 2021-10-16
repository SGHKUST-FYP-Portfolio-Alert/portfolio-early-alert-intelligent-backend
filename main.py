from fastapi import FastAPI
from cron import daily_update_cron
from routes.counterparty import router as CounterpartyRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to root"}


app.include_router(CounterpartyRouter, tags=["Counterparty"], prefix="/counterparty")

scheduler = BackgroundScheduler()
scheduler.add_job(
    daily_update_cron,
    CronTrigger(hour='6')   #trigger 6am everyday.
)
scheduler.start()