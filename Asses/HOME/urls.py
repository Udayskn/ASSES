from django.urls import path
from . import views
app_name='HOME'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('<int:problem_id>',views.ProblemView,name='Problem'),
    path('<int:problem_id>/verdict',views.VerdictView,name = 'verdict')
]