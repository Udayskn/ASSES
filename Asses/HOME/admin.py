from django.contrib import admin

# Register your models here.

from HOME.models import Problem,TestCase,Submission
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)
