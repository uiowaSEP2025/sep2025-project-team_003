from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# @api_view(["POST"])
# def user_create(request):
#     try:
#         new_user = User.objects.create_user(request.data.get('username'), request.data.get('email'), request.data.get('password'))
#         new_user.first_name = request.data.get("firstName")
#         new_user.last_name = request.data.get("lastName")
#         new_user.save()
#     except ValueError as e:
#         return Response({"message": "Invalid values from user inputs"}, status=status.HTTP_400_BAD_REQUEST)
    
#     return Response({"message": "Create new user successfully"}, status=status.HTTP_201_CREATED)

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
    

@api_view(["POST"])
def check_view(request):
    if request.user.is_authenticated:
        return Response({"message": "You are logged in."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You are not logged in."}, status=status.HTTP_401_UNAUTHORIZED)