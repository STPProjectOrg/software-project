from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard_app.views import main, transaction




class TestUrls(SimpleTestCase):

    def test_dashboard_url(self):
        url = reverse("dashboard_app:dashboard")
        self.assertEquals(resolve(url).func, main.dashboard)

    ''' Macht API-Anfrage
    def test_asset_url(self):
        url = reverse("dashboard_app:asset", args=["BTC"])
        self.assertEquals(resolve(url).func, main.asset)
    '''

    def test_transaction_buy_url(self):
        url = reverse("dashboard_app:transaction_buy", args=["BTC"])
        self.assertEquals(resolve(url).func, transaction.buy)

