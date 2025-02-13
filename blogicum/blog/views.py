from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .form import PostForm, CommentForm, CustomUserChangeForm
from .models import Post, Category, Comment

from django.views.generic import CreateView, ListView, UpdateView, DeleteView


def get_published_posts():
    current_time = timezone.now()
    posts = Post.objects.filter(
        Q(is_published=True)
        & Q(category__is_published=True)
        & Q(pub_date__lte=current_time)
    ).select_related('author', 'location', 'category')
    return posts


    
class UserProfile(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = settings.PAGINATOR_PROFILE

    @property
    def get_user(self):
        return get_object_or_404(User, username=self.kwargs['username'])
    
    def get_queryset(self):
        current_user = self.get_user
        if self.request.user == current_user:
            return Post.objects.filter(
                author=current_user
            ).select_related('author', 'location', 'category')
        return get_published_posts().filter(
            author=current_user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user
        return context
        

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
    

class PostBase(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:index'
        )

    def get_queryset(self):
        """Пользователь может работать только со своими комментариями."""
        return self.model.objects.filter(author=self.request.user)

class PostEdit(PostBase, UpdateView):
    form_class = PostForm

    def get_object(self, queryset=None):
        return get_object_or_404(Post, author=self.request.user, pk=self.kwargs['post_id'])

class PostDelete(PostBase, DeleteView):
    def get_object(self, queryset=None):
        return get_object_or_404(Post, author=self.request.user, pk=self.kwargs['post_id'])



class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = settings.PAGINATOR_MAIN_PAGE
    queryset = get_published_posts()


class CategoryList(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = settings.PAGINATOR_CATEGORY_PAGE

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])
    
    def get_queryset(self):
        category = self.get_category()
        if not category.is_published:
            raise Http404('Категория не публикуется!')
        return category.posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        ).select_related('author', 'location')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


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
