from django.views.generic import TemplateView
from django.shortcuts import render


class PageNotFound(TemplateView):
    """Кастомная страница для отображения ошибки 404."""

    template_name = 'pages/404.html'


class IntervalServerErr(TemplateView):
    """Кастомная страница для отображения ошибки 500."""

    template_name = 'pages/500.html'


def csrf_failure(request, reason=''):
    """Кастомная страница для отображения ошибки 403 CSRF."""
    template_name = 'pages/403csrf.html'
    return render(request, template_name, status=403)
