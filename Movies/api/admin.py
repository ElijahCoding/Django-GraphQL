from django.contrib import admin
from .models import Movie, Director

admin.site.register(Director)
admin.site.register(Movie)