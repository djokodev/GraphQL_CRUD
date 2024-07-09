import blog.schemas
import graphene

class Query(blog.schemas.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(blog.schemas.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
