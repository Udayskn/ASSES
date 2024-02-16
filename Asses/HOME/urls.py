from django.urls import path
from . import views
app_name='HOME'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home')
    
]