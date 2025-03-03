import os
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason

class SessionCsrfExemptAuthentication(BaseAuthentication):
    """
    The reason for this class is that DRF auth by default uses session auth, which 
    requires csrf, and there is no way to turn it off. My solution is to write our 
    own auth middleware that disables throwing csrf errors when we don't provide csrf token
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """
        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print('ENV' in os.environ)
        if reason and not 'ENV' not in os.environ:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)



