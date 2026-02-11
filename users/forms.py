from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from cooperatives.models import Cooperative


class CustomUserCreationForm(UserCreationForm):
    last_name = forms.CharField(
        label="Прізвище", widget=forms.TextInput(
            attrs={'placeholder': 'Шевченко'}))
    first_name = forms.CharField(
        label="Ім'я", widget=forms.TextInput(
            attrs={'placeholder': 'Тарас'}))
    middle_name = forms.CharField(
        label="По батькові", required=False, widget=forms.TextInput(
            attrs={'placeholder': 'Григорович'}))
    phone_number = forms.CharField(
        label="📱 Номер телефону",
        widget=forms.TextInput(
            attrs={'placeholder': '+380...'}))
    coop_id = forms.CharField(
        label="🏢 ID Кооперативу", widget=forms.TextInput(
            attrs={'id': 'id_coop_id', 'placeholder': '1'}))
    street = forms.ChoiceField(
        label="📍 Оберіть вашу вулицю",
        widget=forms.Select(attrs={'id': 'id_street'}), required=True)
    house_number = forms.CharField(
        label="🏠 Номер будинку/ділянки", widget=forms.TextInput(
            attrs={'placeholder': '12А'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name', 'middle_name',
                  'phone_number', 'coop_id', 'street', 'house_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = kwargs.get('data') or self.data
        if data and data.get('coop_id'):
            try:
                coop_id = data.get('coop_id')
                cooperative = Cooperative.objects.get(id=coop_id)
                streets = cooperative.street_set.all()
                self.fields['street'].choices = [('',
                                                  '-- Оберіть вулицю --')] + [
                                                    (s.name, s.name) for s in
                                                    streets]
            except (ValueError, TypeError, Cooperative.DoesNotExist):
                self.fields['street'].choices = [('', '---------')]
        else:
            self.fields['street'].choices = [('', '---------')]
