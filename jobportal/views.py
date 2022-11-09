# from django.shortcuts import render
# from .models import Register
# from django.http import HttpResponse
# from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
# import io
# from .models import Register
# from rest_framework.decorators import api_view
# import json
# from django.views.decorators.csrf import csrf_exempt

from .serializers import UserRegistrationSerializer, UserLoginSerialiser, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, UserLogoutSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Genrate Token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # token = get_tokens_for_user(user)
            res= {'msg':'Registration Successful'}
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerialiser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                res= {'token':token,'msg':'Login Successful'}
                return Response(res, status=status.HTTP_200_OK)
            print("error")
        return Response({'errors':{'non_field_errors':['Email And Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            res = {'msg':'change password successful'}
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            res = {
                'msg':'Password reset link send, please check your Email.'
            }
            return Response(res, status=status.HTTP_200_OK)
        

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            res = {'msg': 'reset password set successful'}
            return Response(res, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
    #   logout logic remaining
        print("after post")
        print(request.headers)
        a = request.headers
        print(a['Authorization'])
        a['Authorization']
        # serializer = UserLogoutSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        res = {'msg':'User Logout Successful'}
        return Response(res, status=status.HTTP_204_NO_CONTENT)

# @csrf_exempt
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def register_api(request):
#     if request.method == 'GET':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         print(pythondata, "jsonparser")
#         id = pythondata.get('id', None)
#         if id is not None:
#             reg = Register.objects.get(id=id)
#             serializer = RegisterSerializer(reg)
#             json_data = JSONRenderer().render(serializer.data)
#             # return HttpResponse(json_data, content_type='application/json')
#             return Response(serializer.data)

#         reg = Register.objects.all()
#         serializer = RegisterSerializer(reg, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         print("request post")
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         serializer = RegisterSerializer(data=pythondata)
#         if serializer.is_valid():
#             serializer.save()
#             res = {"msg":"Registration Successful"}
#             json_data = JSONRenderer().render(res)
#             return Response(json_data, status=201)
#         return Response(serializer.errors, status=400)

#     elif request.method == 'PUT':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         print(pythondata)
#         id = pythondata.get('id')
#         reg = Register.objects.get(id=id)
#         print(reg)
#         serializer = RegisterSerializer(reg, data=pythondata, partial=True)
#         if serializer.is_valid():
#             print("valid")
#             serializer.save()
#             res = {"msg","data is updated"}
#             json_data = JSONRenderer().render(res)
#             return Response(json_data, status=201)
#         return Response(serializer.errors, status=400)

#     elif request.method == "DELETE":
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         print(pythondata)
#         id = pythondata.get('id')
#         reg = Register.objects.get(id = id)
#         print(reg)
#         reg.delete()
#         res = {"msg","User is delete"}
#         json_data = JSONRenderer().render(res)
#         # return Response(json_data, status=201)
#         return HttpResponse(json_data, content_type='application/json')


# @api_view(['POST'])
# def login_api(request):
#     if request.method == "POST":
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         print(pythondata)
#         # emailid = pythondata.get('email')
#         # passwd = pythondata.get('password')
#         # acc = Register.objects.filter(email=emailid)
#         # print(acc)
#         res = {"msg","login request goes successfully"}
#         json_data = JSONRenderer().render(res)
#         return Response(json_data, status=201)
