from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.PostCreate.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', views.PostEdit.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/', views.PostDelete.as_view(), name='delete_post'),
    # path('posts/<int:post_id>/comment/', views.CommentCreate.as_view(), name='add_comment'),
    path('category/<slug:category_slug>/',
         views.CategoryList.as_view(), name='category_posts'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('profile/<str:username>', views.UserProfile.as_view(), name='profile'),
]
