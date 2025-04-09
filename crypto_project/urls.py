from django.contrib import admin
from django.urls import path
from crypto_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('get-chart-data/', views.get_chart_data, name='get_chart_data'),
]