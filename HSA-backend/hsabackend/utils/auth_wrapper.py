from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from hsabackend.models.organization import Organization  # change this to match your app name

def check_authenticated_and_onboarded(require_onboarding=True):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                org = Organization.objects.get(owning_User=request.user)
            except Organization.DoesNotExist:
                return Response(
                    {"message": "Organization not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            print(org.is_onboarding)
            if require_onboarding and org.is_onboarding:
                return Response(
                    {"reason": "onboarding"},
                    status=status.HTTP_403_FORBIDDEN
                )

            request.org = org  # attach to request for use in views
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
