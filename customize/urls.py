from . import views
from django.urls import path,include

app_name = 'customize' 

urlpatterns = [
   path('favorite/<str:symbol>/', views.favorite, name='favorite'),
   path('favorite_companies/', views.favorite_companies, name='favorite_companies'),
]