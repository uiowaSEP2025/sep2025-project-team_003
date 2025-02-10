from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def simple_text_response(request):
    return Response("Hello, this is a plain text response!")