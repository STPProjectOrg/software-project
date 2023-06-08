from django.urls import re_path, path
from dashboard_app import views
from dashboard_app.views import main, transaction

app_name = 'dashboard_app'

urlpatterns = [
    re_path('dashboard', main.dashboard, name="dashboard"),
    path('asset/<str:coin>', main.asset, name="asset"),

    # Transaction
    path("transaction/buy", transaction.buy, name="transaction_buy")
]
