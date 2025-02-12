from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def about(request: HttpRequest) -> HttpResponse:
    template_name: str = 'pages/about.html'
    return render(request, template_name)


def rules(request: HttpRequest) -> HttpResponse:
    template_name: str = 'pages/rules.html'
    return render(request, template_name)
