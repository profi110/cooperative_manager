from django import forms
from .models import CooperativeApplication

class CooperativeApplicationForm(forms.ModelForm):
    class Meta:
        model = CooperativeApplication
        fields = ['name', 'address', 'contact_name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Наприклад: ОК "Сонячний"'}),
            'phone': forms.TextInput(attrs={'placeholder': '+380...'}),
        }
