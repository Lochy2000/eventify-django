# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def csrf(request):
    print("CSRF cookie request received")
    return HttpResponse("CSRF cookie set")

@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my drf API!"
    })

@api_view(['POST'])
def logout_route(request):
    print("Logout request received")
    response = Response({"detail": "Successfully logged out."})
    return response
