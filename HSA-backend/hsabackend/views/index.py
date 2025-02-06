# This is a standard passforward to render template + {{ baseURL }}
from django.shortcuts import render

def main_view(request):
    context = {
        'static_url': '/static',
    }
    return render(request, 'index.html', context)