from django.urls import path
from messaging_app import views
app_name = 'messaging_app'

urlpatterns = [
    path('inbox', views.inbox, name="inbox"),
    path('chat/<str:participant>', views.chat, name="chat"),
    #path('message/<str:username>/', views.inbox, name="inbox"),
]