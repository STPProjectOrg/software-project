from core.views import index, landing_page
from django.urls import path

app_name = 'core'
urlpatterns = [
    # Index
    path('', landing_page, name='index'),

    # Landing Page
    path('landing', landing_page, name='landing'),

    # Register

    # Login

]
