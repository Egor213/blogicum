from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView
from blog.form import CustomUserCreationForm
from django.conf import settings
from core.views import PageNotFound, IntervalServerErr

handler404 = PageNotFound.as_view()
handler403 = IntervalServerErr.as_view()

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('blog:index')
        ),
        name='registration'
    ),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),) 