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
                organization = Organization.objects.get(owning_user=request.user)
            except Organization.DoesNotExist:
                raise RuntimeError('No Organization found for the current user')
            
            if require_onboarding and organization.is_onboarding:
                return Response(
                    {"reason": "onboarding"},
                    status=status.HTTP_403_FORBIDDEN
                )

            request.organization = organization  # attach to request for use in views
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
