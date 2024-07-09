import graphene
from graphene_django import DjangoObjectType
from blog.models import Author, Post

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(require=True)
        content = graphene.String(require=True)
        author_id = graphene.ID(required=True)

    post = graphene.Field(PostType) #indique ce que la mutation retournera après avoir été exécutée avec succès.

    def mutate(self, info, title, content, author_id):
        author = Author.objects.get(pk=author_id)
        post = Post(title=title, content=content, author=author)
        post.save()
        return CreatePost(post=post) #Les deux posts sont différents : l'un est un argument passé au constructeur, l'autre est l'instance de Post créée.


class UpdatePost(graphene.Mutation):
    class Argument:
        id = graphene.ID(require=True)
        title = graphene.String(require=True)
        content = graphene.String(require=True)

        post = graphene.Field(PostType)

        def mutate(self, info, id, title=None, content=None):
            try:
                post = Post.objects.get(pk=id)
            except Post.DoesNotExist:
                raise Exception("Post not found")
            
            if title is not None:
                post.title = title
            if content is not None:
                post.content = content

            post.save()
            return UpdatePost(post=post)
        

class DeletePost(graphene.Mutation):
    ...