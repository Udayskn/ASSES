from django.urls import path
from . import views

app_name = 'AUTHENTICATION'
urlpatterns = [
    path('LOGIN/',views.login_func,name = 'login'),
    path('SIGNIN/',views.signin_func,name='signin')
]