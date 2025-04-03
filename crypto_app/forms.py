from django import forms

class CryptoAnalysisForm(forms.Form):
    symbol = forms.CharField(
        label='Símbolo da Criptomoeda (ex: BTC, ETH)',
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )