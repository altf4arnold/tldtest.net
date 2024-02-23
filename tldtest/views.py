from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'home.html'

def home(request):
    return render(request, 'home.html')

"""
def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)

"""
