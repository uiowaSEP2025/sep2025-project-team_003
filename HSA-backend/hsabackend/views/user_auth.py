from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

@api_view(["POST"])
def loginView(request):
    user_name = request.data.get('username','')
    password = request.data.get('password', '')
    print(user_name,password)
    user = authenticate(username=user_name, password=password)
    if user:
        login(request, user)
        return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)