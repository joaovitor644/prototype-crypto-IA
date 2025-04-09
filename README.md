# Análise de Investimento em Criptomoedas com IA

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.1-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-brightgreen.svg)

Um sistema inteligente para análise e recomendação de investimentos em criptomoedas utilizando Django e a API da OpenAI.

## 🚀 Funcionalidades Principais

- ✅ Análise em tempo real de criptomoedas
- ✅ Recomendações de compra/venda baseadas em IA
- ✅ Previsões de valorização (3/6/12 meses)
- ✅ Classificação de risco (baixo/médio/alto)


## 📦 Pré-requisitos

- Python 3.10+
- Django 5.1+
- Conta na [CoinMarketCap](https://coinmarketcap.com/api/)
- Chave de API da [OpenAI](https://platform.openai.com/)
- Chave de API da [NewsAPI](https://newsapi.org/)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/joaovitor644/prototype-crypto-IA.git
cd prototype-crypto-IA
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o `.env` com suas chaves de API:
```
OPENAI_API_KEY=sua_chave_aqui
COINMARKETCAP_API_KEY=sua_chave_aqui
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## 🌐 Uso

Acesse `http://localhost:8000` no seu navegador e:

1. Insira o símbolo da criptomoeda (ex: BTC, ETH)
2. Clique em "Analisar"
3. Veja a recomendação detalhada gerada pela IA

## 🛡️ Tratamento de Erros

O sistema inclui mecanismos robustos para lidar com:
- Erros de conexão com APIs externas
- Respostas inesperadas da OpenAI
- Formatação inválida de dados
- Fallback automático para manter a aplicação funcional

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

