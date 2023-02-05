from core.views import debug, index, landing_page
from django.urls import path

app_name = 'core'
urlpatterns = [
    # Debug
    path('debug', debug, name='debug'),
    path('bootstraü', )
    
    # Index
    path('', landing_page, name='index'),

    # Landing Page
    path('landing', landing_page, name='landing'),

    # Register

    # Login

]
