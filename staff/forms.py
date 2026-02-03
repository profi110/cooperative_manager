from django import forms
from users.models import CustomUser
from cooperatives.models import Membership

class UserUpdateForm(forms.ModelForm):
    """Форма для персональних даних користувача"""
    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'username', 'phone_number']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MembershipUpdateForm(forms.ModelForm):
    """Форма для даних про членство в кооперативі"""
    class Meta:
        model = Membership
        fields = ['street', 'plot_number', 'role']
        widgets = {
            'street': forms.Select(attrs={'class': 'form-control'}),
            'plot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }