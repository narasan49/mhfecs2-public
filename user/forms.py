from django import forms
from .models import User

class UserProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ("name", "self_introduce", "Url", "UrlTitle", "UrlDescription")
