from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, ProfileForm
from .mixins import CommentMixin, PostMixin, PostUpdateDeleteMixin
from .models import Category, Post, User
from .modules import get_posts, get_published_posts


class ProfileUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    model = User
    template_name = 'blog/user.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile",
            args=[self.request.user]
        )


class IndexListView(
    ListView
):
    template_name = 'blog/index.html'
    paginate_by = settings.COUNT_POSTS
    queryset = get_published_posts(
    ).annotate(
        comment_count=Count("comments")
    ).order_by(
        '-pub_date'
    )


class CategoryListView(
    ListView
):
    template_name = 'blog/category.html'
    paginate_by = settings.COUNT_POSTS

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        posts = category.posts.select_related(
            'author',
            'location',
            'category'
        ).filter(
            is_published=True,
            pub_date__lt=timezone.now(),
        ).annotate(
            comment_count=Count("comments")
        ).order_by(
            '-pub_date'
        )
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context


class PostDetailView(
    DetailView
):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            get_posts(),
            pk=self.kwargs[self.pk_url_kwarg]
        )
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            get_published_posts(),
            pk=self.kwargs[self.pk_url_kwarg]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related(
                'author'
            )
        )
        return context


class PostCreateView(
    LoginRequiredMixin,
    PostMixin,
    CreateView
):
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:profile", args=[self.request.user])


class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    PostMixin,
    PostUpdateDeleteMixin,
    UpdateView
):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return redirect('blog:post_detail', self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            args=[self.kwargs[self.pk_url_kwarg]]
        )


class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    PostMixin,
    PostUpdateDeleteMixin,
    DeleteView
):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return redirect('blog:post_detail', self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            args=[self.request.user]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context


class UserListVieW(
    ListView
):
    template_name = 'blog/profile.html'
    paginate_by = settings.COUNT_POSTS

    def get_queryset(self):
        queryset = get_posts(
        ).filter(
            author__username=self.kwargs['username']
        ).annotate(
            comment_count=Count("comments")
        ).order_by(
            '-pub_date'
        )
        if str(self.request.user) == self.kwargs['username']:
            return queryset
        return get_published_posts(
        ).filter(
            author__username=self.kwargs['username']
        ).annotate(
            comment_count=Count("comments")
        ).order_by(
            '-pub_date'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class CommentCreateView(
    LoginRequiredMixin,
    CommentMixin,
    CreateView
):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            get_published_posts(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail",
            args=[self.kwargs['post_id']]
        )


class CommentUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CommentMixin,
    UpdateView
):
    pk_url_kwarg = "comment_id"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return redirect('blog:post_detail', self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail",
            args=[self.kwargs['post_id']]
        )


class CommentDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CommentMixin,
    DeleteView
):
    pk_url_kwarg = "comment_id"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return redirect('blog:post_detail', self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail",
            args=[self.kwargs['post_id']]
        )
