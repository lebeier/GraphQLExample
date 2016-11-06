from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='books')

    def __str__(self):
        return self.name
