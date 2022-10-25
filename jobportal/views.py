from django.shortcuts import render
from .models import Register
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io
from .models import Register
from .serializers import RegisterSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def register_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print(pythondata, "jsonparser")
        id = pythondata.get('id', None)
        if id is not None:
            reg = Register.objects.get(id=id)
            serializer = RegisterSerializer(reg)
            json_data = JSONRenderer().render(serializer.data)
            # return HttpResponse(json_data, content_type='application/json')
            return Response(serializer.data)

        reg = Register.objects.all()
        serializer = RegisterSerializer(reg, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("request post")
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = RegisterSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {"msg":"Registration Successful"}
            json_data = JSONRenderer().render(res)
            return Response(json_data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print(pythondata)
        id = pythondata.get('id')
        reg = Register.objects.get(id=id)
        print(reg)
        serializer = RegisterSerializer(reg, data=pythondata, partial=True)
        if serializer.is_valid():
            print("valid")
            serializer.save()
            res = {"msg","data is updated"}
            json_data = JSONRenderer().render(res)
            return Response(json_data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print(pythondata)
        id = pythondata.get('id')
        reg = Register.objects.get(id = id)
        print(reg)
        reg.delete()
        res = {"msg","User is delete"}
        json_data = JSONRenderer().render(res)
        # return Response(json_data, status=201)
        return HttpResponse(json_data, content_type='application/json')


@api_view(['POST'])
def login_api(request):
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        print(pythondata)
        # emailid = pythondata.get('email')
        # passwd = pythondata.get('password')
        # acc = Register.objects.filter(email=emailid)
        # print(acc)
        res = {"msg","login request goes successfully"}
        json_data = JSONRenderer().render(res)
        return Response(json_data, status=201)
