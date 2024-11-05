from django.db import models

class TodoItem(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)

# Create your models here.
