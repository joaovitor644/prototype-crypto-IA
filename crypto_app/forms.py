from django import forms

class CryptoAnalysisForm(forms.Form):
    symbol = forms.CharField(
        label='Digite o que deseja saber',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )