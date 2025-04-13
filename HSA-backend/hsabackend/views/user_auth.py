from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from hsabackend.views.organizations import createOrganization


@api_view(["POST"])
def user_exist(request):
    username = request.data.get('username')
    email = request.data.get('email')

    if not username and not email:
        return Response({"message": "At least one of username or email must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    query = Q()
    
    if username:
        query |= Q(username=username)
    if email:
        query |= Q(email__iexact=email)

    is_existed =  User.objects.filter(query).exists()

    if (is_existed):
        return Response({"message": "User existed"}, status=status.HTTP_409_CONFLICT)
    else:
        return Response({"message": "User is availble to create"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_create(request):
    organization_info = request.data.get('organizationInfo')
    username = request.data.get('username')
    email = request.data.get('email')

    User = get_user_model()
    query = Q()

    if username:
        query |= Q(username=username)
    if email:
        query |= Q(email__iexact=email)

    is_existed =  User.objects.filter(query).exists()

    if is_existed:
        return Response({"message": "User existed"}, status=status.HTTP_409_CONFLICT)
    
    try:
        new_user = User.objects.create_user(request.data.get('username'), request.data.get('email'), request.data.get('password'))
        new_user.first_name = request.data.get("firstName")
        new_user.last_name = request.data.get("lastName")
        new_user.save()

        createOrganization(organization_info)
    except ValueError as e:
        return Response({"message": "Invalid values from user inputs"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Create new user successfully"}, status=status.HTTP_201_CREATED)

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
    
