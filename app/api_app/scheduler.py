import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.settings import TIME_ZONE
from .views import getAllCoinsFromDatabase, saveDataFromApiToDatabase


# Der scheduler wird mit dieser Methode gestartet.
# Die Funktion update_data() wird jeden Tag um 01:00 Uhr ausgeführt.
def start_scheduler():
    scheduler = BackgroundScheduler(timezone=TIME_ZONE)
    scheduler.add_job(
        update_data,
        'cron',
        day_of_week="mon-sun",
        hour=1,
    )
    try:
        scheduler.start()
    except Exception as e:
        print(f"Error starting dailyScheduler: {e}")


# Diese Funktion wird vom Scheduler aufgerufen.
def update_data():
    print("scheduler: API DATA UPDATE INITIALIZED")
    for concreteCurrency in getAllCoinsFromDatabase():
        saveDataFromApiToDatabase(concreteCurrency.name ,'EUR', dateFrom=datetime.date.today(), dateTo=datetime.date.today())
        # GETCURRENTCRYPTOPRICE
