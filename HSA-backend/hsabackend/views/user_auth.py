from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate


@api_view(["POST"])
def login(request):
    user_name = request.GET.get('password','')
    password = request.GET.get('password', '')
    user = authenticate(username="john", password="secret")
    return Response("Hello, this is a plain text response!")