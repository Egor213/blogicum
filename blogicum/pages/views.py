from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "pages/about.html"


class RulesView(TemplateView):
    template_name = "pages/rules.html"


def page_not_found(request, exception):
    template_name = "pages/404.html"
    return render(request, template_name, status=404)


def internal_server_err(request):
    template_name = "pages/500.html"
    return render(request, template_name, status=500)


def csrf_failure(request, reason=""):
    template_name = "pages/403csrf.html"
    return render(request, template_name, status=403)
