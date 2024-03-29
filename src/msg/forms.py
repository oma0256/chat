from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )

    class Meta:
        model = Message
        fields = ['message']
