from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post, Category

from django.views.generic import DetailView


def get_published_posts():
    current_time = timezone.now()
    posts = Post.objects.filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=current_time)
    ).select_related('author', 'location', 'category')
    return posts

class UserProfile(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'blog/profile.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = get_published_posts().filter(
            author=self.get_object()
        )
        return context





def index(request: HttpRequest) -> HttpResponse:
    template_name = 'blog/index.html'
    posts = get_published_posts()[:5]
    context = {'post_list': posts}
    return render(request, template_name, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    template_name = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404('Категория не публикуется!')
    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {
        'category': category_slug,
        'post_list': posts
    }
    return render(request, template_name, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    current_time = timezone.now()
    if post.pub_date > current_time:
        raise Http404('Данная запись еще не опубликована!')
    if not post.is_published or not post.category.is_published:
        raise Http404('Публикация недоступна!')
    context = {
        'post': post
    }
    return render(request, template_name, context)

