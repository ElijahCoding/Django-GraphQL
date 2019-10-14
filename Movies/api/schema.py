import graphene
from graphene_django.types import DjangoObjectType
from .models import Director, Movie

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()


