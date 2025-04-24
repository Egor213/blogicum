from django.db.models import Count
from django.http import Http404
from django.views import generic
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .form import PostForm, CommentForm, CustomUserChangeForm
from .models import Post, Category, Comment


User = get_user_model()


def get_annotated_posts(queryset):
    return queryset.annotate(comment_count=Count("comments")).order_by(
        *Post._meta.ordering
    )


def get_published_posts(object):
    current_time = timezone.now()
    return get_annotated_posts(
        object.filter(
            Q(is_published=True)
            & Q(pub_date__lte=current_time)
            & Q(category__is_published=True)
        ).select_related("author", "location", "category")
    )


class PostModelMixin(LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs["post_id"])


class DispatchPostMixin(PostModelMixin):
    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]}
        )

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return redirect("blog:post_detail", post_id=kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)


class CommentBaseMixin(DispatchPostMixin):
    model = Comment
    template_name = "blog/comment.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs["comment_id"])


class UserProfileView(generic.ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = settings.PAGINATOR_PROFILE

    @property
    def get_user(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_queryset(self):
        current_user = self.get_user
        if self.request.user == current_user:
            return get_annotated_posts(
                Post.objects.filter(author=current_user).select_related(
                    "author", "location", "category"
                )
            )
        return get_published_posts(Post.objects).filter(author=current_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_user
        return context


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostEditView(DispatchPostMixin, generic.UpdateView):
    pass


class PostDeleteView(DispatchPostMixin, generic.DeleteView):
    def get_success_url(self):
        return reverse_lazy("blog:index")


class PostCreateView(PostModelMixin, generic.CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = settings.PAGINATOR_MAIN_PAGE
    queryset = get_published_posts(Post.objects)


def post_detail(request, post_id):
    template_name = "blog/detail.html"
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm(request.POST)
    current_time = timezone.now()
    if post.author != request.user:
        if not post.is_published or not post.category.is_published:
            raise Http404("Публикация недоступна!")
        elif post.pub_date > current_time:
            raise Http404("Данная запись еще не опубликована!")
    comments = post.comments.all()
    context = {"post": post, "comments": comments, "form": comment_form}
    return render(request, template_name, context)


class CommentUpdateView(CommentBaseMixin, generic.UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentBaseMixin, generic.DeleteView):
    pass


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
    return redirect("blog:post_detail", post_id=post_id)


class CategoryListView(generic.ListView):
    model = Category
    template_name = "blog/category.html"
    paginate_by = settings.PAGINATOR_CATEGORY_PAGE

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs["category_slug"])

    def get_queryset(self):
        category = self.get_category()
        if not category.is_published:
            raise Http404("Категория не публикуется!")
        return get_published_posts(category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context
