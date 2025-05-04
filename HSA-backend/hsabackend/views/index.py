# This is a standard pass forward to render template + {{ baseURL }}
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def main_view(request):
    context = {
        'static_url': '/static',
    }
    return render(request, 'index.html', context)