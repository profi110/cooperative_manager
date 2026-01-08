from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from cooperatives.models import Cooperative

class CustomUserCreationForm(UserCreationForm):
    cooperative = forms.ModelChoiceField(
        queryset=Cooperative.objects.all(),
        label="Оберіть ваш кооператив",
        required=True,
        empty_label="-- Натисніть, щоб вибрати --"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'cooperative')