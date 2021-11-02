from fastapi import FastAPI
from cron import daily_update_cron
from routes.counterparty import router as CounterpartyRouter
from routes.news import router as NewsRouter
from routes.calculation import router as CalculationRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://fyp.cslix1.ml",
    "https://fyp.richardng.nets.hk"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["Accept", "Content-Type"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to root"}


app.include_router(CounterpartyRouter, tags=["Counterparty"], prefix="/counterparty")
app.include_router(NewsRouter, tags=["News"], prefix="/news")
app.include_router(CalculationRouter, tags=["Calculation"], prefix="/calculation")

scheduler = BackgroundScheduler()
scheduler.add_job(
    daily_update_cron,
    CronTrigger(hour='6')   #trigger 6am everyday.
)
scheduler.start()