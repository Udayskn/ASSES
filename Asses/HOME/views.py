from django.shortcuts import render
from HOME.models import Problem
from django.views import generic
# Create your views here.
class HomeView(generic.ListView):
    template_name = 'HOME/home.html'
    context_object_name = 'Problem_list'

    def get_queryset(self):
        return Problem.objects.all()