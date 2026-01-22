from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from cooperatives.models import Cooperative, Street


class CustomUserCreationForm(UserCreationForm):
    coop_id = forms.CharField(
        label="🏢 ID Кооперативу",
        widget=forms.TextInput(
            attrs={'id': 'id_coop_id', 'placeholder': 'Наприклад: 1'})
        )

    street = forms.CharField(
        label="📍 Оберіть вашу вулицю",
        widget=forms.Select(attrs={'id': 'id_street'}),
        required=True
        )
    house_number = forms.CharField(
        label="🏠 Номер будинку",
        widget=forms.TextInput(attrs={'placeholder': 'Наприклад: 12А'})
        )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'coop_id', 'street', 'house_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'coop_id' in self.data:
            try:
                coop_id = self.data.get('coop_id')
                cooperative = Cooperative.objects.get(id=coop_id)
                streets = cooperative.street_set.all()
                self.fields['street'].widget.choices = [(s.name, s.name) for s
                                                        in streets]
            except (ValueError, TypeError, Cooperative.DoesNotExist):
                pass
