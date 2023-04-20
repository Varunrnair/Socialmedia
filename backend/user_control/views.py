from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(APIView):
    # authentication_classes=[JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            people = serializer.save()
            return Response({'status': 'success', 'user_id': people.id})
        else:
            return Response(serializer.errors, status=400)

class LoginView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            people = authenticate(request, email=email, password=password)
            if people is not None:
                login(request, people)
                return Response({'status': 'success'})
            else:
                return Response({'status': 'failed', 'message': 'Invalid credentials'}, status=401)
        else:
            return Response(serializer.errors, status=400)
        
class display(APIView):
    serializer_class=UserSerializer
    def get(self,request):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
        