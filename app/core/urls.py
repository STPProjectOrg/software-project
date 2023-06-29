""" Routes for the core_app """

from django.urls import path
from core.views import (debug, index, landing_page, legal_disclosure,
                        privacy, cookie_disclosure, search_results, question_and_answers)

# Configuration
app_name = 'core'

# Routes
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

    # Cookie Disclosure
    path('question-and-answers', question_and_answers, name='qaa'),

    # Search results
    path('search/', search_results, name='search_results')

]
