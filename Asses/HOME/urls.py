from django.urls import path
from . import views
app_name='HOME'
urlpatterns = [
    path('',views.HomeView.as_view(),name='Home'),
    path('<int:problem_id>',views.ProblemView,name='Problem'),
    path('<int:problem_id>/verdict',views.VerdictView,name = 'Verdict'),
    path('addProblem',views.addProblem,name='AddProblem'),
    path('addTestCase',views.addTestCase,name='NameTestCase')
]