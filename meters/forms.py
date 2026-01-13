from django import forms
from .models import Reading


class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ['meter', 'value_total', 'value_day', 'value_night', 'photo']
        widgets = {
            'value_total': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Загальний'}),
            'value_day': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'День (Т1)'}),
            'value_night': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ніч (Т2)'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            }
        labels = {
            'value_total': 'Загальний показник',
            'value_day': 'День',
            'value_night': 'Ніч',
            'photo': 'Фото підтвердження',
            }

    def clean(self):
        cleaned_data = super().clean()

        total = cleaned_data.get("value_total")
        day = cleaned_data.get("value_day")
        night = cleaned_data.get("value_night")

        if day is not None and night is not None:
            calculated_sum = day + night

            if total != calculated_sum:
                raise forms.ValidationError(
                    f"Помилка! Сума День ({day}) + Ніч ({night}) дорівнює {calculated_sum}, "
                    f"а ви ввели Загальний {total}. Перевірте цифри."
                    )

        return cleaned_data
