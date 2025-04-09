from django import forms

class CryptoAnalysisForm(forms.Form):
    symbol = forms.CharField(
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'prompt-box'})
    )