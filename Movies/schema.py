import graphene
import Movies.api.schema

class Query(Movies.api.schema.Query, graphene.ObjectType):
    pass

class Mutation(Movies.api.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)