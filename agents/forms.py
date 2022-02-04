from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

user = get_user_model()

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = user
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'department',
            'user_type',
            'manager',
            'user_role',
            'profile_picture'
        )
        