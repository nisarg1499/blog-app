from django.utils.functional import cached_property
from .loaders import BlogsByAuthorIdLoader

class GQLContext:
    
    def __init__(self, request):
        self.request = request
    
    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def blogs_by_author_id_loader(self):
        return BlogsByAuthorIdLoader()