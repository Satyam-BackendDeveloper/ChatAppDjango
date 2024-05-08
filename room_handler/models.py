from django.db import models

# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=100, unique=True)
    description=models.CharField(max_length=100, null=True, blank=True)
    port=models.IntegerField(help_text="contains port for websocket connection", null=True, blank=True)