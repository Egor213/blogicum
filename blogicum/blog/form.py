from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment

User = get_user_model()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', )