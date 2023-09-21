
from datetime import date
from django.test import TestCase
from django.urls import reverse, resolve
from api_app.cryptoservice import save_data_from_api_to_database
from api_app.models import AssetHistory
from dashboard_app.models import Transaction
from dashboard_app.models import Watchlist
from dashboard_app.views import main, transaction
from django.contrib.auth import get_user_model
from api_app.cryptoservice import add_asset_to_database
from api_app.models import Asset

User = get_user_model()
class TestUrls(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.watchlist = Watchlist.objects.create(
            user = self.user
        )
        self.client.login(username='testuser', password='testpassword')
        Asset.objects.get_or_create(name="BTC", coinName="Bitcoin", imageUrl="https://www.cryptocompare.com/media/37746251/btc.png")
        self.asset = Asset.objects.get_or_create(name="BTC")[0]
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-20'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-19'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-18'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-17'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-16'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-15'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-14'),
            value = 25000,
            name = self.asset
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-13'),
            value = 25000,
            name = self.asset
        )
        self.transaction = Transaction.objects.create(
            user = self.user,
            asset = self.asset,
            purchaseDate = date.fromisoformat('2023-05-20'),
    	    amount = 2,
            price = 50000,
            tax = 12,
            charge = 10,
            cost = 50022
        )

    def test_asset(self):
        response = self.client.get(reverse('dashboard_app:asset', args=['BTC',7]))
        self.assertEqual(response.status_code, 200)

    def test_coin_overview(self):
        response = self.client.get(reverse('dashboard_app:coin_overview', args=['no_sort','n']))
        self.assertEqual(response.status_code, 200)

    def test_watchlist(self):
        response = self.client.get(reverse('dashboard_app:watchlist', args=['testuser','no_sort','n']))
        self.assertEqual(response.status_code, 200)

    def test_watchlist_add(self):
        response = self.client.get(reverse('dashboard_app:watchlist_add', args=['BTC']))
        self.assertEqual(response.status_code, 302)

    def test_watchlist_price_change(self):
        response = self.client.get(reverse('dashboard_app:watchlist_update_asset_price_change', args=['BTC',7]))
        self.assertEqual(response.status_code, 302)

    def test_transactions(self):
        response = self.client.get(reverse('dashboard_app:transactions'))
        self.assertEqual(response.status_code, 200)

    def test_transactions_add(self):
        response = self.client.post(reverse('dashboard_app:transaction_add',args=['BTC']), {"sell": False, "price":24000,"date":date.fromisoformat('2023-05-20'),"amount":1,"charge":10,"tax":5, "cost": 24015, "post":False, "postText": ""})
        self.assertEqual(response.status_code, 302)

    def test_transactions_update(self):
        response = self.client.post(reverse('dashboard_app:transaction_update',args=[1]), {"price":24000,"date":date.fromisoformat('2023-05-20'),"amount":1,"charge":10,"tax":5, "cost": 24015})
        self.assertEqual(response.status_code, 302)

    def test_transactions_delete(self):
        response = self.client.get(reverse('dashboard_app:transaction_delete', args=[1]))
        self.assertEqual(response.status_code, 302)

    

