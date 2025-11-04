from django import forms
from .models import Choice


class AnswerForm(forms.Form):
    choice_id = forms.ModelChoiceField(
        queryset=Choice.objects.none(),  # view içinde set edilecek
        empty_label=None,
        widget=forms.RadioSelect(attrs={"class": "choice"})
    )


