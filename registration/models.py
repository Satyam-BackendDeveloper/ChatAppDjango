from django.db import models
from django.contrib.auth.models import User
class ContactList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cl_owner')
    contacts = models.ManyToManyField(User)
