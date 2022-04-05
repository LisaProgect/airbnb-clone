from django.contrib import admin
from .models import Conversation, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message Admin Definition"""


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Conversation Admin Definition"""
