from django.urls import path
from conversations.views import ConversationDetailView, go_conversation

app_name = "conversations"

urlpatterns = [
    path("go/<int:host_pk>/<int:guest_pk>/", go_conversation, name="go"),
    path("<int:pk>/", ConversationDetailView.as_view(), name="detail"),
]
