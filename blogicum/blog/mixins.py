from .forms import CommentForm, PostForm
from .models import Comment
from .modules import get_posts


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'


class PostMixin:
    template_name = 'blog/create.html'
    form_class = PostForm


class PostUpdateDeleteMixin:
    pk_url_kwarg = 'post_id'
    queryset = get_posts()
