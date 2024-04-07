from django.db import models

# Create your models here.
class Results(models.Model):
    title = models.TextField()
    abstract = models.TextField()
    algorithm = models.TextField()
    methodology = models.TextField()
    results = models.TextField()

    def __str__(self):
        return self.title