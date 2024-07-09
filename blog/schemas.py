import graphene
from blog.models import Author, Post
from blog.type import PostType, AuthorType


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    post = graphene.Field(PostType) #indique ce que la mutation retournera après avoir été exécutée avec succès.

    def mutate(self, info, title, content, author_id):
        author = Author.objects.get(pk=author_id)
        toto = Post.objects.create(title=title, content=content, author=author)
        return CreatePost(post=toto) #Les deux posts sont différents : l'un est un argument passé au constructeur, l'autre est l'instance de Post créée.


class UpdatePost(graphene.Mutation):
    class Argument:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)

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
    class Argument:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        
        post.delete()
        return DeletePost(success=True)
    

class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    authors = graphene.List(AuthorType)

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_authors(self, info):
        return Author.objects.all()
    

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)