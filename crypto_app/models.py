from django.db import models

class CryptoAnalysis(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    analysis_date = models.DateTimeField(auto_now_add=True)
    recommendation = models.CharField(max_length=20)  # 'buy', 'hold', 'sell'
    confidence = models.FloatField()  # 0-1
    price_prediction = models.JSONField()  # {'3_months': 50%, '6_months': 75%}
    risk_level = models.CharField(max_length=20)  # 'low', 'medium', 'high'
    analysis_summary = models.TextField()
    raw_data = models.JSONField()  # Dados brutos da API
    
    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.recommendation}"