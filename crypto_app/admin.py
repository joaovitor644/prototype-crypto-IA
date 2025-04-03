from django.contrib import admin
from .models import CryptoAnalysis

@admin.register(CryptoAnalysis)
class CryptoAnalysisAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'recommendation', 'risk_level', 'analysis_date')
    list_filter = ('recommendation', 'risk_level')
    search_fields = ('symbol', 'name')
    readonly_fields = ('analysis_date',)