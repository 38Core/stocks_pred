from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('mypage/', views.mypage, name='mypage'),
    path('logout/', views.logout_view, name='logout'), 
    path('', include('django.contrib.auth.urls')),
]