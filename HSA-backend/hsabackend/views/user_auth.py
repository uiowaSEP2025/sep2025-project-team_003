from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from hsabackend.models.organization import Organization
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.hashers import make_password
from hsabackend.utils.api_validators import password_strength_validator

@api_view(["POST"])
def user_exist(request):
    username = request.data.get('username')
    email = request.data.get('email')

    if not username and not email:
        return Response({"message": "At least one of username or email must be provided."}, status=status.HTTP_400_BAD_REQUEST)

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

    if not organization_info:
        return Response({"message": "Missing organization info"}, status=status.HTTP_400_BAD_REQUEST)

    query = Q()

    if username:
        query |= Q(username=username)
    if email:
        query |= Q(email__iexact=email)

    is_existed =  User.objects.filter(query).exists()

    if is_existed:
        return Response({"message": "User existed"}, status=status.HTTP_409_CONFLICT)
    
    req_password = request.data.get('password')

    if not password_strength_validator(req_password):
        return Response({"message": "Password is not strong enough"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(req_password)

    new_user = User(email=request.data.get('email'),username=request.data.get('username'), password=hashed_password)
    try:
        new_user.full_clean()

        with transaction.atomic():
            new_user.save()
            new_org = Organization(
                org_name = organization_info.get("name"),
                org_email = organization_info.get("email"),
                org_city = organization_info.get("city"),
                org_requestor_state = organization_info.get("requestorState"),
                org_requestor_zip = organization_info.get("requestorZip"),
                org_requestor_address = organization_info.get("requestorAddress"),
                org_phone = organization_info.get("phone", "").replace("-", ""),
                org_owner_first_name = organization_info.get("ownerFn"),
                org_owner_last_name = organization_info.get("ownerLn"),
                owning_User = new_user
            )
            new_org.full_clean()
            new_org.save()

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
    
