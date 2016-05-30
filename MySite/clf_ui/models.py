from django.db import models

# Create your models here.


class Comment(models.Model):
    clf_type = models.Charfield(initial='Paste comment', max_length=1000)
    classifiers = models.MultipleChoiceField()



