from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, ChangePasswordView, UpdateUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh' ),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_user/<int:pk>/', UpdateUserView.as_view(), name='auth_update_user')
]
