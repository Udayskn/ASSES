from django.db import models

# Create your models here.
class Problem(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField()
    diff_level=models.CharField(max_length=20)

    def __str__(self):
        return self.name
