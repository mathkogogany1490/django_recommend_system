from django.contrib import admin
from chatbot.models import ChatBot
# Register your models here.

@admin.register(ChatBot)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'genre')
    search_fields = ['genre']
    list_filter = ['genre']