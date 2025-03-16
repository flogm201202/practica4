from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


class Library(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    author = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.author} - {self.library}"


class User(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"user: {self.name}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # pone la fecha actual, cuando se presta, que es cuando se crea un objet loabn
    date_start = models.DateField(auto_now_add=True)
    # ingresar la fecha en que se devuelve
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Loan: book:{self.book}; user: {self.user}; period:{self.date_start}-{self.date_end}"
