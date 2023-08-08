from .models import Post


def get_posts():
    return Post.objects.select_related(
        'location',
        'author',
        'category'
    )


def get_published_posts():
    return Post.published_posts.select_related(
        'location',
        'author',
        'category'
    )
