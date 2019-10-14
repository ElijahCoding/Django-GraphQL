import graphene
from graphene_django.types import DjangoObjectType
from .models import Director, Movie

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old movie" if self.year < 200 else "New movie"

class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())

    all_directors = graphene.List(DirectorType)

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Movie.objects.get(pk=id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None

    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()
    
