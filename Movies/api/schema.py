import graphene
from graphene import relay
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
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


# Relay Implementation
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'year': ['exact', ]
        }
        interfaces = (relay.Node,)
    
    
class Query(graphene.ObjectType):
    # all_movies = graphene.List(MovieType)
    # movie = graphene.Field(MovieType, id=graphene.Int(), title=graphene.String())
    all_movies = DjangoFilterConnectionField(MovieNode)
    movie = relay.Node.Field(MovieNode)
    
    all_directors = graphene.List(DirectorType)
    
    # @login_required
    # def resolve_all_movies(self, info, **kwargs):
    #     return Movie.objects.all()

    # def resolve_movie(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     title = kwargs.get('title')
    # 
    #     if id is not None:
    #         return Movie.objects.get(pk=id)
    # 
    #     if title is not None:
    #         return Movie.objects.get(title=title)
    # 
    #     return None

    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()

class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)
    
    movie = graphene.Field(MovieType)
    
    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)
        return MovieCreateMutation(movie=movie)

class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.Int()
    
    movie = graphene.Field(MovieType)
    
    def mutate(self, info, id, title, year):
        movie = Movie.objects.get(pk=id)
        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year
        movie.save()

        return MovieUpdateMutation(movie=movie)

class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()

        return MovieDeleteMutation(movie=None)
        
class Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()