from django.urls import path
from .views import \
    ChangePasswordView, \
    UpdateUserView, \
    RegisterView, \
    LogoutView, \
    LogoutAllView, \
    TokenObtainPairView # MyTokenObtainPairView, custom field not supported by blacklist 


from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh' ),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    # path('update_user/<int:pk>/', UpdateUserView.as_view(), name='auth_update_user'),
    path('update_user/<username>/', UpdateUserView.as_view(), name='auth_update_user'), # to lookup by username instead of pk
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all')
]
