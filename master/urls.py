from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views

app_name = 'master' 

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('master_page/', views.master_page, name='master_page'),
    path('company_search_list/', views.company_search_list, name='company_search_list'),
    path('company_read/<str:symbol>/', views.company_read, name='company_read'),

    path('company_create/', views.company_create, name='company_create'),
    path('company_create_result/<str:symbol>/', views.company_create_result, name='company_create_result'),

    path('company_delete/<str:symbol>/', views.company_delete, name='company_delete'),
    path('company_delete_result/', views.company_delete_result, name='company_delete_result'),
    
    path('company_update/<str:symbol>/', views.company_update, name='company_update'),
    path('company_update_result/<str:symbol>/', views.company_update_result, name='company_update_result'),
]