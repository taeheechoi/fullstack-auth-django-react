from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes= (AllowAny,)

class ChangePasswordView(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)


class UpdateUserView(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_REST_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        
        return Response(status=status.HTTP_205_RESET_CONTENT)
