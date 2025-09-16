

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:chat_id>/', views.home, name='home'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
