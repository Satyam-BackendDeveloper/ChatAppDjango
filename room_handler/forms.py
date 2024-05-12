from django import forms
from .models import Room
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class JoinRoomForm(forms.Form):
    room_name = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label=None)
    user_name = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        room_name = cleaned_data.get("room_name")
        user_name = cleaned_data.get("user_name")

        try:
            Room.objects.get(room_name=room_name.room_name)
        except Room.DoesNotExist:
            raise ValidationError({"room_name": f"Room {room_name} does not exist"})

        try:
            User.objects.get(username=user_name)
        except User.DoesNotExist:
            raise ValidationError({"user_name": f"User {user_name} does not exist"})


class ChatRoomForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'message-input'}))
