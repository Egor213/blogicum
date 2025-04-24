from django.forms import ModelForm, DateInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post, Comment

User = get_user_model()


class UserFormMixin:
    model = User
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
        exclude = ("author", "comment_count")
        widgets = {"pub_date": DateInput(attrs={"type": "date"})}


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserFormMixin, UserCreationForm.Meta):
        pass


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserFormMixin, UserChangeForm.Meta):
        pass
