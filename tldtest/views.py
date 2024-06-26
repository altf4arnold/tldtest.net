from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from tldtester.models import TLD


class Index(ListView):
    model = TLD
    template_name = 'home.html'

    def get_queryset(self):
        """
        Tutorial for this is on https://learndjango.com/tutorials/django-search-tutorial
        When writing more optimized search things, might be good reference
        """
        object_list = TLD.objects.all().order_by('tld')
        return object_list


class About(TemplateView):
    template_name = 'about.html'


class Latency(TemplateView):
    template_name = 'latency.html'


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
