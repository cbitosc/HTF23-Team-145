from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('accounts', views.accounts, name = 'Accounts'),
    path('delacc/<str:acc>', views.delacc,name = 'delacc' ),
    path('del/<str:type>/<str:name>', views.delpage, name = 'del'),
    path('login',views.login_view, name = 'login' ),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name = 'register')

] 
