# myapp/middleware.py
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect

class AboutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('about'):
            return HttpResponseRedirect(reverse('hello_world'))
        return self.get_response(request)
