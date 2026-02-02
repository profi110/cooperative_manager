from django import forms
from .models import Reading


class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ['value_total', 'value_day', 'value_night', 'photo']
        widgets = {
            'value_total': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'value_day': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'value_night': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            }

    def __init__(self, *args, **kwargs):
        self.is_two_zone = kwargs.pop('is_two_zone', False)
        super().__init__(*args, **kwargs)

        self.fields['photo'].required = False

        if not self.is_two_zone:
            self.fields['value_day'].widget = forms.HiddenInput()
            self.fields['value_night'].widget = forms.HiddenInput()
            self.fields['value_day'].required = False
            self.fields['value_night'].required = False
