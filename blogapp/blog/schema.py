import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene import ObjectType, List
from .models import Blog
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime

class BlogType(DjangoObjectType):
    class Meta:
        model = Blog

class UserType(DjangoObjectType):
    blogs = List(BlogType)
    class Meta:
        model = get_user_model()
        use_connection = True

    def resolve_blogs(root, info, **kwargs):
        return info.context.blogs_by_author_id_loader.load(root.id)


class Query(graphene.ObjectType):
    blogs = graphene.List(BlogType)
    login = graphene.Field(UserType, username=graphene.String(), password=graphene.String())
    authorblogs = graphene.List(BlogType, username=graphene.String())
    # user = DjangoConnectionField(UserType)
    allAuthorBlogs = DjangoConnectionField(UserType)

    def resolve_allAuthorBlogs(root, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_blogs(self, info, **kwargs):
        all_blogs = Blog.objects.all()
        return all_blogs

    def resolve_login(self, info, username, password, **kwargs):
        auth_user = authenticate(username=username, password=password)

        if auth_user == None:
            raise Exception("Invalid Credentials")

        return auth_user

    def resolve_authorblogs(self, info, username, **kwargs):
        user = get_user_model().objects.get(username=username)

        get_blogs = Blog.objects.filter(author=user)
        
        return get_blogs

class CreateBlog(graphene.Mutation):
    createBlog = graphene.Field(BlogType)

    class Arguments:
        username = graphene.String(required=True)
        title = graphene.String(required=True)
        blog_data = graphene.String(required=True)

    def mutate(self, info, username:str, title: str, blog_data: str, **kwargs):
        user = get_user_model().objects.get(username=username)

        blog = Blog(author=user, title=title, created_at=datetime.now(), blog_data=blog_data)
        blog.save()

        return CreateBlog(createBlog=blog)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)

    def mutate(self, info, username: str, password: str, email: str, firstName: str, lastName: str):

        user = get_user_model()(
            username=username, email=email, first_name=firstName, last_name=lastName
        )
        user.set_password(password)

        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_blog = CreateBlog.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)