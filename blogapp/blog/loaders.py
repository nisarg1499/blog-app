from collections import defaultdict
from promise import Promise
from promise.dataloader import DataLoader
from .models import Blog
from django.contrib.auth import get_user_model

class BlogsByAuthorIdLoader(DataLoader):
    def batch_load_fn(self, author_ids):
        blogs_by_author_id = defaultdict(list)
        for blog in Blog.objects.filter(author_id__in=author_ids).iterator():
            blogs_by_author_id[blog.author_id].append(blog)

        return Promise.resolve([blogs_by_author_id.get(author_id, []) for author_id in author_ids])