from datetime import date
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import F,Sum
from api_app.models import Asset, AssetHistory
from dashboard_app.models import Transaction, Watchlist

User = get_user_model()
class TestViews(TestCase):
    
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
        asset_1 = Asset.objects.get_or_create(name="BTC")[0]
        Asset.objects.get_or_create(name="ETH", coinName="Ethereum", imageUrl="https://www.cryptocompare.com/media/37746238/eth.png")
        asset_2 = Asset.objects.get_or_create(name="ETH")[0]
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-20'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-19'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-18'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-17'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-16'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-15'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-14'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-13'),
            value = 25000,
            name = asset_1
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-20'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-19'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-18'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-17'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-16'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-15'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-14'),
            value = 140,
            name = asset_2
        )
        AssetHistory.objects.create(
            date = date.fromisoformat('2023-05-13'),
            value = 140,
            name = asset_2
        )
        self.transaction_btc_1 = Transaction.objects.create(
            user = self.user,
            asset = asset_1,
            purchaseDate = date.fromisoformat('2023-05-20'),
    	    amount = 2,
            price = 50000,
            tax = 12,
            charge = 10,
            cost = 50022
        )
        self.transaction_eth_1 = Transaction.objects.create(
            user = self.user,
            asset = asset_2,
            purchaseDate = date.fromisoformat('2023-05-20'),
    	    amount = 2,
            price = 280,
            tax = 12,
            charge = 10,
            cost = 302
        )
        self.transaction_btc_2 = Transaction.objects.create(
            user = self.user,
            asset = asset_1,
            purchaseDate = date.fromisoformat('2023-05-18'),
    	    amount = 1,
            price = 25000,
            tax = 12,
            charge = 10,
            cost = 25022
        )
        self.transaction_eth_2 = Transaction.objects.create(
            user = self.user,
            asset = asset_2,
            purchaseDate = date.fromisoformat('2023-05-16'),
    	    amount = 4,
            price = 560,
            tax = 12,
            charge = 10,
            cost = 582
        )

    def test_dashboard (self):
        compare_pie = {'data': [75000.0, 840.0], 'labels': ['Bitcoin', 'Ethereum'], 'symbols': ['BTC', 'ETH']}
        compare_line = {'button_values': {'1week': 134.42857142857142, '1month': 134.42857142857142, '6month': 134.42857142857142, '1year': 134.42857142857142, 'all': 134.42857142857142}, 'data': [560.0, 560.0, 25560.0, 25560.0, 75840.0], 'labels': ['16.05.2023', '17.05.2023', '18.05.2023', '19.05.2023', '20.05.2023']}
        compare_kpi = {'invested': 75840.0, 'tax': 48.0, 'charge': 40.0, 'total': 75840.0, 'cost': 75928.0, 'profit': -88.0}
        compare_assets = Asset.objects.filter(transaction__user=self.user).annotate(
            amount=Sum("transaction__amount"),
            cost=Sum("transaction__cost"),
            total_value=F("amount") * F("price"),
            profit=F("total_value") - F("cost")
        ).distinct()
        response = self.client.get(reverse('dashboard_app:dashboard', args=['0']))
        context = response.context

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/dashboard.html')
        self.assertEqual(context['pie_data'], compare_pie)
        self.assertEqual(context['line_data'], compare_line)
        self.assertEqual(context['kpi'], compare_kpi)
        self.assertQuerysetEqual(context['assets'], compare_assets, ordered=False, transform=lambda x: x)

    def test_asset(self):
        test_asset = Asset.objects.get_or_create(name="BTC")[0]
        test_line_data = {'button_values': {'1week': 0.0, '1month': 0.0, '6month': 0.0, '1year': 0.0, 'all': 0.0}, 'data': [25000.0, 25000.0, 25000.0, 25000.0, 25000.0, 25000.0, 25000.0], 'labels': ['14.05.2023', '15.05.2023', '16.05.2023', '17.05.2023', '18.05.2023', '19.05.2023', '20.05.2023']}
        self.client.get(reverse('dashboard_app:watchlist_add', args=['BTC']))
        response = self.client.get(reverse('dashboard_app:asset', args=['BTC',7]))
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/asset.html')
        self.assertEqual(context["asset"], test_asset)
        self.assertEqual(context["asset_in_watchlist"], True)
        self.assertEqual(context["line_data"], test_line_data)

    def test_watchlist(self):
        self.client.get(reverse('dashboard_app:watchlist_add', args=['BTC']))
        response = self.client.get(reverse('dashboard_app:watchlist', args=['testuser','no_sort','n']))
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/watchlist.html')
        self.assertEqual(len(context["watchlist"]), 1)
        self.assertEqual(context["watchlist"][0]["name"], "BTC")
        self.assertEqual(context["watchlist"][0]["isInWatchlist"], True)
        self.assertEqual(context["watchlist"][0]["isInPortfolio"], True)
        self.assertEqual(context["username"], self.user.username)
        self.assertEqual(context["is_own_watchlist"], True)
        self.assertEqual(context["watchlist_privacy_settings"], "all")

    def test_transactions(self):
        response = self.client.get(reverse('dashboard_app:transactions'))
        context = response.context
        test_transactions = Transaction.objects.filter(
        user=self.user.id).order_by("-purchaseDate")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/transactions.html')
        self.assertQuerysetEqual(context["transactions"], test_transactions, ordered=False, transform=lambda x: x)

    def test_coin_overview(self):
        response = self.client.get(reverse('dashboard_app:coin_overview', args=['no_sort','n']))
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_app/coins_overview.html')
        self.assertEqual(context['coins'][0]["name"], "BTC")
        self.assertEqual(context['coins'][1]["name"], "ETH")

