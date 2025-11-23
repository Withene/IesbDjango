from django.urls import path
from . import views

app_name = 'apiv1'

urlpatterns = [
    path('ping/', views.health_check, name='ping'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('users-list/', views.users_list_view, name='users_list')
]
