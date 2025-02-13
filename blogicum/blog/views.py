from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .form import PostForm, CommentForm, CustomUserChangeForm
from .models import Post, Category, Comment

from django.views.generic import CreateView, ListView, UpdateView, DeleteView


def get_published_posts(object):
    current_time = timezone.now()
    return object.filter(
            Q(is_published=True)
            & Q(pub_date__lte=current_time)
        ).select_related('author', 'location', 'category')


    
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
        return get_published_posts(Post.objects).filter(
            Q(author=current_user)
            & Q(category__is_published=True)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user
        return context
        

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
    

class PostLoginModelMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'


class PostBaseMixin(PostLoginModelMixin):
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )
    
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return redirect(
                'blog:post_detail',
                post_id=kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
    
    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])


class PostEdit(PostBaseMixin, UpdateView):
    form_class = PostForm


class PostDelete(PostBaseMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(
            'blog:index'
        )
    
class PostCreate(PostLoginModelMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = settings.PAGINATOR_MAIN_PAGE
    queryset = get_published_posts(Post.objects).filter(
        category__is_published=True
    )


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
        return get_published_posts(category.posts)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm(request.POST)
    current_time = timezone.now()
    if post.author != request.user:
        if not post.is_published or not post.category.is_published:
            raise Http404('Публикация недоступна!')
        elif post.pub_date > current_time:
            raise Http404('Данная запись еще не опубликована!')
    comments = post.comments.all()
    context = {
        'post': post,
        'comments': comments,
        'form': comment_form
    }
    return render(request, template_name, context)
    

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        post.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdate(UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment, pk=self.kwargs['comment_id']
        )
    
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return redirect(
                'blog:post_detail',
                post_id=kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment, pk=self.kwargs['comment_id']
        )
    
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return redirect(
                'blog:post_detail',
                post_id=kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )