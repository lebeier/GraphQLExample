from graphene import AbstractType
from graphene import Field
from graphene import Node
from graphene import ClientIDMutation
from graphene import String
from graphene import Float

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql_relay.node.node import from_global_id

from .models import Category
from .models import Book

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node, )
        filter_fields = ['name', 'books']
        filter_order_by = ['name']

class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (Node, )
        filter_fields = ['name']
        filter_order_by = ['name']

class NewCategory(ClientIDMutation):
    category = Field(CategoryNode)
    class Input:
        name = String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Category(
             name = input.get('name') ,
        )
        temp.save()
        return NewCategory(category=temp)

class NewBook(ClientIDMutation):
    book = Field(BookNode)
    class Input:
        name = String()
        author = String()
        category = String()
    
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        book = Book(
            name = input.get('name'),
            author = input.get('author'),
            category = Category.objects.get(name=input.get('category'))            
        )
        book.save()
        return NewBook(book=book)

class UpdateBook(ClientIDMutation):
    book = Field(BookNode)
    class Input:
        id = String()
        name = String()
        author = String()
    
    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        book = Book.objects.get(pk=from_global_id(input.get('id'))[1])
        book.name=input.get('name')
        book.author=input.get('author')
        book.save()
        return UpdateBook(book=book)

class CategoryMutation(AbstractType):
    new_category = NewCategory.Field()

class BookMutation(AbstractType):
    new_Book = NewBook.Field()
    update_book = UpdateBook.Field()

class CategoryQuery(AbstractType):
     category = DjangoFilterConnectionField(CategoryNode)
 
class BookQuery(AbstractType):
     book = Node.Field(BookNode)
     all_books = DjangoFilterConnectionField(BookNode)
