from django.contrib import admin
from .models import ContactList

class ContactListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContactList._meta.fields]
    list_filter = [field.name for field in ContactList._meta.fields]
    search_fields = [field.name for field in ContactList._meta.fields]

admin.site.register(ContactList, ContactListAdmin)

