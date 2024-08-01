from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout, authenticate
from .serializers import UserSerializer, DepositSerializer, WithdrawSerializer
from .models import CustomUser

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not (username or email) or not password:
            return Response({'error': 'Username or email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password) or authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.auth.delete()  # Deletes the token associated with the current user
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class DepositView(generics.GenericAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            request.user.deposit(amount)
            return Response({'message': 'Deposit successful', 'new_balance': request.user.security_deposit}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawView(generics.GenericAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            if request.user.withdraw(amount):
                return Response({'message': 'Withdrawal successful', 'new_balance': request.user.security_deposit}, status=status.HTTP_200_OK)
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
