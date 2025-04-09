import requests
import random
import json
import httpx
from django.conf import settings
from openai import OpenAI
from django.http import JsonResponse
from datetime import datetime, timedelta

def get_random_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": settings.COINMARKETCAP_API_KEY,
    }
    params = {
        "start": 1,
        "limit": 50,  # Obter os dados das 50 principais criptomoedas
        "convert": "USD",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        cryptos = data.get("data", [])
        # Selecionar uma criptomoeda aleatória
        random_crypto = random.choice(cryptos)
        return {
            "name": random_crypto["name"],
            "symbol": random_crypto["symbol"],
            "price": random_crypto["quote"]["USD"]["price"],
            "price_change_24h": random_crypto["quote"]["USD"]["percent_change_24h"],
            "market_cap": random_crypto["quote"]["USD"]["market_cap"],
            "all_time_high": random_crypto.get("max_supply", "N/A"),  # Alta histórica aproximada
        }
    except requests.RequestException as e:
        print(f"Erro ao buscar dados da API CoinMarketCap: {e}")
        return None
    

def get_crypto_chart_data(request):
    symbol = request.GET.get("symbol", "BTC")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "X-CMC_PRO_API_KEY": settings.COINMARKETCAP_API_KEY,
    }
    params = {"symbol": symbol}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Get the cryptocurrency full name
        crypto_data = data["data"].get(symbol)
        if not crypto_data:
            return JsonResponse({"success": False, "error": "Symbol not found in API response."})

        crypto_name = crypto_data.get("name", "Unknown")

        # Generate dynamic dates for the last 30 days
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%d %b") for i in range(30)][::-1]

        # Current price of the cryptocurrency
        price = data["data"][symbol]["quote"]["USD"]["price"]

        # Generate mock data with realistic percentage variations for 30 days
        historical_prices = []
        current_price = price
        for _ in range(30):
            # Simulate small daily price changes (±5%)
            daily_change = random.uniform(-0.05, 0.05)
            current_price = round(current_price * (1 + daily_change), 2)
            historical_prices.append(current_price)

        return JsonResponse({
            "success": True,
            "prices": historical_prices[::-1],  # Ensure oldest-to-newest order
            "dates": dates,  # Use dynamically generated dates
            "name": crypto_name,
        })
    except requests.RequestException as e:
        return JsonResponse({"success": False, "error": str(e)})
    
def get_crypto_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "cryptocurrency",  # Palavras-chave para filtrar notícias
        "apiKey": settings.NEWS_API_KEY,  # Substitua pela sua chave da News API
        "language": "en",  # Idioma das notícias
        "sortBy": "publishedAt",  # Ordenar por data de publicação
        "pageSize": 5,  # Quantidade de notícias
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        return [
            {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
            }
            for article in articles
        ]
    except requests.RequestException as e:
        print(f"Erro ao buscar notícias: {e}")
        return []

def get_crypto_data(symbol):
    """Obtém dados da criptomoeda da CoinMarketCap API"""
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {'symbol': symbol, 'convert': 'USD'}
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.COINMARKETCAP_API_KEY,
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['data'][symbol]
    except Exception as e:
        print(f"Error fetching crypto data: {str(e)}")
        return None

def analyze_with_llm(crypto_data):
    """Versão completamente robusta da análise com LLM"""
    try:
        # Configuração simplificada do cliente
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Prompt mais estruturado para garantir resposta JSON válida
        prompt = f"""
        ANALISE ESTES DADOS DE CRIPTOMOEDA E RETORNE UM JSON:

        Dados:
        {json.dumps(crypto_data, indent=2)}

        ESTRUTURA REQUERIDA:
        {{
            "recommendation": "(comprar/segurar/vender)",
            "confidence": (0.0-1.0),
            "price_prediction": {{
                "3_months": "(X%)",
                "6_months": "(X%)",
                "1_year": "(X%)"
            }},
            "risk_level": "(baixo/médio/alto)",
            "analysis_summary": "(análise detalhada em português)"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo mais recente com melhor suporte a JSON
            response_format={"type": "json_object"},  # Força resposta em JSON
            messages=[
                {"role": "system", "content": "Você é um analista financeiro. Retorne APENAS o JSON solicitado."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # Menos criatividade para respostas mais consistentes
        )

        if response.choices:
            content = response.choices[0].message.content
            # Limpeza básica da resposta
            content = content.strip().replace('```json', '').replace('```', '')
            return json.loads(content)
        
        return None

    except json.JSONDecodeError:
        print("A API retornou uma resposta não-JSON válida")
        return {
            "recommendation": "hold",
            "confidence": 0.5,
            "price_prediction": {
                "3_months": "0%",
                "6_months": "0%",
                "1_year": "0%"
            },
            "risk_level": "medium",
            "analysis_summary": "Erro na análise. Por favor, tente novamente."
        }
    except Exception as e:
        print(f"Erro na análise: {str(e)}")
        return None