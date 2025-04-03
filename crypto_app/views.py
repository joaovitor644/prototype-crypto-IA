from django.shortcuts import render, redirect
from .forms import CryptoAnalysisForm
from .models import CryptoAnalysis
from .utils import get_crypto_data, analyze_with_llm
import json

def index(request):
    if request.method == 'POST':
        form = CryptoAnalysisForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()
            
            # Obtém dados da API
            crypto_data = get_crypto_data(symbol)
            if not crypto_data:
                return render(request, 'crypto_app/index.html', {
                    'form': form,
                    'error': 'Não foi possível obter dados para esta criptomoeda.'
                })
            
            # Analisa com LLM
            analysis = analyze_with_llm(json.dumps(crypto_data, indent=2))
            if not analysis:
                return render(request, 'crypto_app/index.html', {
                    'form': form,
                    'error': 'Erro ao analisar os dados.'
                })
            
            # Salva no banco de dados
            crypto_analysis = CryptoAnalysis(
                symbol=symbol,
                name=crypto_data['name'],
                recommendation=analysis['recommendation'],
                confidence=analysis['confidence'],
                price_prediction=analysis['price_prediction'],
                risk_level=analysis['risk_level'],
                analysis_summary=analysis['analysis_summary'],
                raw_data=crypto_data
            )
            crypto_analysis.save()
            
            return render(request, 'crypto_app/analysis.html', {
                'analysis': crypto_analysis
            })
    else:
        form = CryptoAnalysisForm()
    
    return render(request, 'crypto_app/index.html', {'form': form})