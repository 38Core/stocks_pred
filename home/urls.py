from django.urls import path
from . import views

#アプリフォルダ名{ %'アプリ名':パスのニックネーム % }
from django.urls import path,include

app_name = 'home' 

urlpatterns = [
    path('',views.index,name='index'),
]