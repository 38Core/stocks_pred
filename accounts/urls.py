from django.urls import path
from . import views

#アプリフォルダ名{ %'アプリ名':パスのニックネーム % }
from django.urls import path,include

app_name = 'accounts' 

urlpatterns = [
    #デフォルトの認証URL
    path('', include('django.contrib.auth.urls')),
    #ユーザー登録ページ
    path('cleate/', views.cleate, name='cleate'),
]