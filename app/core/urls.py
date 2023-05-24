from core.views import debug, index, landing_page, legal_disclosure, privacy, cookie_disclosure
from django.urls import path

app_name = 'core'
urlpatterns = [
    # Debug
    path('debug', debug, name='debug'),

    # Index
    path('', index, name='index'),

    # Landing Page
    path('landing',  landing_page, name='landing'),

    # Legal Disclosure
    path('impressum', legal_disclosure, name='legal_disclosure'),

    # Privacy
    path('datenschutz', privacy, name='privacy'),

    # Cookie Disclosure
    path('cookies', cookie_disclosure, name='cookie_disclosure'),

    # Register


    # Login

]
