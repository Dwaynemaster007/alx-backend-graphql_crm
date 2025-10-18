import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

schema = graphene.Schema(query=Query)

class Query(CRMQuery, graphene.ObjectType)

from crm.schema import
