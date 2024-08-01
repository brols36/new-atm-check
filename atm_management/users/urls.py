from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, DepositView, WithdrawView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('deposit/', DepositView.as_view(), name='user_deposit'),
    path('withdraw/', WithdrawView.as_view(), name='user_withdraw'),
]
