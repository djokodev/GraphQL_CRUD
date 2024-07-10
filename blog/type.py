from graphene_django import DjangoObjectType
from blog.models import Author, Post
from graphene import relay


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = ['title', 'content']
        interfaces = (relay.Node, )

class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = ['name']
        interfaces = (relay.Node, )


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"