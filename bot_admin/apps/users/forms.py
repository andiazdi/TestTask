from django import forms

class BroadcastMessageForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 60}),
        label="Сообщение для отправки",
    )