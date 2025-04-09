from django import forms

class CryptoAnalysisForm(forms.Form):
    symbol = forms.CharField(
        label='Digite sua pergunta sobre criptomoedas ou digite o código da moeda para obter uma analise:',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'prompt-box'})
    )