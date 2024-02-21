from HOME.models import Problem
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from HOME.forms import CodeForm
from django.conf import settings

# Create your views here.
class HomeView(generic.ListView):
    template_name = 'HOME/home.html'
    context_object_name = 'Problem_list'

    def get_queryset(self):
        return Problem.objects.all()
def ProblemView(request, problem_id):
    #template_name='HOME/problem.html'
    problem = get_object_or_404(Problem, id=problem_id)
    #form = CodeForm()
    context = {
        'ProblemName': problem.name,
        'Problemstatement': problem.description,
        'problem_id': id,
        'problem': problem,
    }
    return render(request, 'HOME\problem.html', context)