from django.db import models

class ChatBot(models.Model):
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
    genre = models.CharField(max_length=100)
