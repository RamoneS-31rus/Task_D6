from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'post_author': ['exact'],
                  'post_type': ['exact'],
                  'post_category': ['exact'],
                  'post_title': ['icontains'],
                  'post_time': ['range'],
                  }
