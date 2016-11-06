import graphene
from books.schema import BookQuery
from books.schema import CategoryQuery
from books.schema import BookMutation
from books.schema import CategoryMutation

class RootQuery(BookQuery
        , CategoryQuery
        , graphene.ObjectType):
    pass

class RootMutation(BookMutation
        , CategoryMutation
        , graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)

