from django.contrib import admin
from django.urls import include, path
from core.views import PageNotFound, IntervalServerErr

handler404 = PageNotFound.as_view()
handler403 = IntervalServerErr.as_view()

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
]
