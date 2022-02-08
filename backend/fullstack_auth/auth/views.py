from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer, UserDetailSerializer
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
    # lookup_field = 'username' # no needed cuz user id exists in self.context['request'].user.id


class UpdateUserView(generics.UpdateAPIView):
    queryset=User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    # lookup_field = 'username' # no needed cuz user id exists in self.context['request'].user.id

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     print(self.request.user.id)
    #     return User.objects.filter(id=self.request.user.id)

    def get(self, request):
        try:
            # user = User.objects.filter(id=request.user.id)[0]
            # status_code = status.HTTP_200_OK
            # response = {
            #     'success': 'true',
            #     'status code': status_code,
            #     'message': 'User profile fetched successfully',
            #     'data': [{
            #         'username': user.username,
            #         'first_name': user.first_name,
            #         'last_name': user.last_name,
            #         'email': user.email,
            #         }]
            # }
            user = User.objects.filter(id=request.user.id).first()
            return Response([{
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }], status=status.HTTP_200_OK)

        except Exception as e:
            # status_code = status.HTTP_400_BAD_REQUEST
            # response = {
            #     'success': 'false',
            #     'status code': status.HTTP_400_BAD_REQUEST,
            #     'message': 'User does not exists',
            #     'error': str(e)
            #     }
        # return Response(response, status=status_code)
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
