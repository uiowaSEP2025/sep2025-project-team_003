from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

@api_view(["POST"])
def login_view(request):
    user_name = request.data.get('username','')
    password = request.data.get('password', '')
    user = authenticate(username=user_name, password=password)
    if user:
        login(request, user)
        return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["POST"])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You are not logged in."}, status=status.HTTP_400_BAD_REQUEST)