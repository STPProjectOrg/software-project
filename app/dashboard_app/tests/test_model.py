from datetime import date
import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from api_app.cryptoservice import add_asset_to_database
from api_app.models import Asset
from dashboard_app.models import Transaction,Watchlist,WatchlistAsset

pytestmark = pytest.mark.django_db
User = get_user_model()

class TestModelInstances(TestCase):
    def test_transaction(self):
        transaction = mixer.blend('dashboard_app.Transaction')
        assert transaction.pk == 1, 'Should create a Tranaction instance'

    def test_watchlist(self):
        watchlist = mixer.blend('dashboard_app.Watchlist')
        assert watchlist.pk == 1, 'Should create a Tranaction instance'

    def test_watchlist_asset(self):
        watchlist_asset = mixer.blend('dashboard_app.WatchlistAsset')
        assert watchlist_asset.pk == 1, 'Should create a WatchlistAsset instance'

class TransactionModelTest(TestCase):
    def setUp(self):
        add_asset_to_database("BTC","EUR")
        test_asset = Asset.objects.get_or_create(name="BTC")[0]
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )

        self.transaction = Transaction.objects.create(
            user = test_user,
            asset = test_asset,
            purchaseDate = date.today(),
    	    amount = 2,
            price = 50000,
            tax = 12,
            charge = 10,
            cost = 50022
        )

    def test_create_transaction(self):
        self.assertEqual(self.transaction.user.username,'testuser')
        self.assertEqual(self.transaction.asset.coinName,'Bitcoin')
        self.assertEqual(self.transaction.purchaseDate,date.today())
        self.assertEqual(self.transaction.amount,2)
        self.assertEqual(self.transaction.price,50000)
        self.assertEqual(self.transaction.tax,12)
        self.assertEqual(self.transaction.charge,10)
        self.assertEqual(self.transaction.cost,50022)


class WatchlistModelTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )
        self.watchlist = Watchlist.objects.create(
            user = test_user
        )
    
    def test_create_watchlist(self):
        self.assertEqual(self.watchlist.user.username,'testuser')
        self.assertEqual(self.watchlist.privacy_settings,'all')

class WatchlistAssetModelTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )
        test_watchlist = Watchlist.objects.create(
            user = test_user
        )
        add_asset_to_database("BTC","EUR")
        test_asset = Asset.objects.get_or_create(name="BTC")[0]
        self.watchlistAsset=WatchlistAsset.objects.create(
            watchlist = test_watchlist,
            asset = test_asset,
            added_at = date.today()
        )
    
    def test_create_watchlistAsset(self):
        self.assertEqual(self.watchlistAsset.watchlist.user.username,'testuser')
        self.assertEqual(self.watchlistAsset.asset.coinName,'Bitcoin')
        self.assertEqual(self.watchlistAsset.added_at,date.today())
        self.assertEqual(self.watchlistAsset.price_change,30)


        