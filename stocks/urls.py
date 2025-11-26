from . import views
from django.urls import path,include

app_name = 'stocks' 

urlpatterns = [
    path('search_company/', views.search_company, name='search_company'), 
    path('company_list/', views.company_list, name='company_list'), 
    path('<str:symbol>/', views.stock_chart, name='stock_chart'),  
]
