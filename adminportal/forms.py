from django import forms
from .models import email


class EmailForm(forms.ModelForm):
    class Meta:
        model = email
        fields = ['recipient', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 10}),
        }
