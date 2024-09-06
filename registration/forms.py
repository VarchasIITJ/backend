from django import forms
from .models import TeamRegistration


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = TeamRegistration
        fields = ['sport', 'college']

    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"


class RemovePlayerForm(forms.Form):
    player = forms.CharField()
