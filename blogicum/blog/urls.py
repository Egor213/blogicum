from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path(
        "profile/edit/", views.ProfileEditView.as_view(), name="edit_profile"
    ),
    path(
        "profile/<str:username>/",
        views.UserProfileView.as_view(),
        name="profile",
    ),
    path(
        "category/<slug:category_slug>/",
        views.CategoryListView.as_view(),
        name="category_posts",
    ),
    path("posts/create/", views.PostCreateView.as_view(), name="create_post"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path(
        "posts/<int:post_id>/comment/",
        views.comment_create,
        name="add_comment",
    ),
    path(
        "posts/<int:post_id>/edit/",
        views.PostEditView.as_view(),
        name="edit_post",
    ),
    path(
        "posts/<int:post_id>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
]
