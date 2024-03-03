from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Problem(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField()
    diff_level=models.CharField(max_length=20)

    def __str__(self):
        return self.name
class Submission(models.Model):
    problem = models.ForeignKey(Problem,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    user_code = models.CharField(max_length = 10000,default='')
    verdict = models.CharField(max_length = 100,default='Wrong Answer')
    lang_choices = [
        ('python','python'),
        ('C','C'),
        ('C++','C++')
    ]
    language = models.CharField(max_length = 100,choices = lang_choices)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    input = models.CharField(max_length=1000)
    output = models.CharField(max_length=1000)