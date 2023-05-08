import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.settings import TIME_ZONE
from .views import addCoinToDatabase

# Wir bräuchten hier eine Liste mit allen Coins, die wir in der Datenbank haben wollen.
allCurrencys = {
    '0': {
        'identifier': 'BTC',
        'name': 'Bitcoin',
        'currency': 'EUR'
    }
}


# Der scheduler wird mit dieser Methode gestartet.
# Die Funktion update_data() wird jeden Tag um 03:00 Uhr ausgeführt.
def start_scheduler():
    scheduler = BackgroundScheduler(timezone=TIME_ZONE)
    scheduler.add_job(
        update_data,
        'cron',
        day_of_week="mon-sun",
        hour=3
    )
    scheduler.start()


# Diese Funktion wird vom Scheduler aufgerufen.
# Der Aufruf der Methode addCoinToDatabase() fügt die Coins der Datenbank hinzu.
# Eventuell müssen die Fehler noch gefangen werden. -> Mit Julian besprechen
def update_data():
    print("scheduler: NEW API UPDATE INITIALIZED")
    for i in range(len(allCurrencys)):
        concreteCurrency = allCurrencys.get("%i" % i)
        print(allCurrencys)
        print(concreteCurrency)
        addCoinToDatabase(
            concreteCurrency.get('identifier'),
            concreteCurrency.get('name'),
            concreteCurrency.get('currency')
        )
        # GETCURRENTCRYPTOPRICE
