from django.apps import AppConfig
from django.contrib import admin
from .models import Author, Book

class ApiConfig(AppConfig):
    name = 'api'

admin.site.register(Author)
admin.site.register(Book)