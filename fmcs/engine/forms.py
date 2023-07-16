from django import forms

from .models import Tournament, Participant


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'format', 'start_date', 'swiss_rounds']
        widgets = {
            'swiss_rounds': forms.NumberInput(attrs={'min': 0}),
            # Устанавливаем минимальное значение 0 для swiss_rounds
        }

    def clean_swiss_rounds(self):
        format = self.cleaned_data.get('format')
        swiss_rounds = self.cleaned_data.get('swiss_rounds')
        if format == 'swiss' and swiss_rounds is None:
            raise forms.ValidationError("For Swiss System, the number of rounds is required.")
        return swiss_rounds


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'tournament']  # Добавляем поле tournament в список полей

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tournament'].widget = forms.HiddenInput()  # Скрываем поле от пользователя
        self.fields['tournament'].required = False  # Делаем поле необязательным
