from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from jobportal.serializers import UserRegistrationSerializer, UserLoginSerialiser, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, UserLogoutSerializer

from jobportal.views import get_tokens_for_user

# Create your views here.
def register(request):
    return HttpResponse("Hello async world!")

class EmployerRegisterView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = { 'msg' : 'Registration Succeful'}
            return Response(res, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        serializer = UserRegistrationSerializer()
        res= {'msg':'Login Successful'}
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployerLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_employer == True:
                    print("user is employer")
                else:
                    return Response({'msg': 'You are not employer'}, status=status.HTTP_401_UNAUTHORIZED)
                token = get_tokens_for_user(user)
                res= {'token':token, 'msg':'Login Successful'}
                return Response(res, status=status.HTTP_200_OK)
        return  Response({'errors':{'non_field_errors':['Email And Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
