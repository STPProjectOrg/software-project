import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.settings import TIME_ZONE
from .databaseservice import get_all_assets_from_database
from .cryptoservice import save_data_from_api_to_database

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


def update_data():
    print("scheduler: API DATA UPDATE INITIALIZED")
    for concreteCurrency in get_all_assets_from_database():
        save_data_from_api_to_database(concreteCurrency.name ,
                                  'EUR', 
                                  date_from=datetime.date.today(), 
                                  date_to=datetime.date.today())
