from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from cooperatives.models import Cooperative


class CustomUserCreationForm(UserCreationForm):
    last_name = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={'placeholder': 'Наприклад: Шевченко'})
        )
    first_name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={'placeholder': 'Наприклад: Тарас'})
        )
    middle_name = forms.CharField(
        label="По батькові",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Наприклад: Григорович'})
        )
    phone_number = forms.CharField(
        label="📱 Номер телефону",
        widget=forms.TextInput(attrs={'placeholder': '+380...'})
        )

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
        label="🏠 Номер будинку/ділянки",
        widget=forms.TextInput(attrs={'placeholder': 'Наприклад: 12А'})
        )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username', 'email', 'last_name', 'first_name',
            'middle_name', 'phone_number', 'coop_id', 'street', 'house_number'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs[
                'class'] = f"{existing_class} form-control".strip()

        if 'coop_id' in self.data:
            try:
                coop_id = self.data.get('coop_id')
                cooperative = Cooperative.objects.get(id=coop_id)
                streets = cooperative.street_set.all()
                self.fields['street'].widget.choices = [(s.name, s.name) for s
                                                        in streets]
            except (ValueError, TypeError, Cooperative.DoesNotExist):
                self.fields['street'].widget.choices = [('', '---------')]
        else:
            self.fields['street'].widget.choices = [('', '---------')]
