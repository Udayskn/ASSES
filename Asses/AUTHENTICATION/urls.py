from django.urls import path
from . import views

app_name = 'AUTHENTICATION'
urlpatterns = [
    path('login/',views.login_func,name = 'Login'),
    path('signup/',views.signin_func,name='Signup')
]