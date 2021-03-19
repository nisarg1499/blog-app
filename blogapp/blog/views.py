from django.shortcuts import render
from graphene_django.views import GraphQLView
from .context import GQLContext


class CustomGraphQLView(GraphQLView):

    def get_context(self, request):
        return GQLContext(request)