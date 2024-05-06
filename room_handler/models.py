from django.db import models

# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=100, unique=True)
    description=models.CharField(max_length=100, null=True, blank=True)