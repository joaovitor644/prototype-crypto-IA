import requests
import json
import httpx
from django.conf import settings
from openai import OpenAI

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