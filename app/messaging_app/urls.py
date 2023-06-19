from django.urls import path
from messaging_app import views
app_name = 'messaging_app'

urlpatterns = [
    path('inbox', views.inbox, name="inbox"),
    path('inbox/<str:participant_req>', views.inbox_chat, name="inbox-chat"),
]