from django.urls import path
from messaging_app.views import inbox_chat, inbox, messages
app_name = 'messaging_app'

urlpatterns = [
    # Main
    path('inbox', inbox.inbox, name="inbox"),

    # Chat
    path('inbox/<str:participant_req>', inbox_chat.inbox_chat, name="inbox_chat"),
    path('inbox/add_message/<str:chat_participant_name>', messages.create_message, name="create_message"),
]