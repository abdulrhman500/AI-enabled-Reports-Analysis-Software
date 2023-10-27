from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, PatchSerializer, SubmissionsSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password, validate_patch
from main.models import AppUser,Patch,Submissions
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os
from rest_framework.parsers import FileUploadParser,MultiPartParser, FormParser

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		if "error" in clean_data.keys():
			return JsonResponse(clean_data, status=500)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				serializer = UserLoginSerializer(data=clean_data)
				if serializer.is_valid(raise_exception=True):
					send_mail("A.I.E.I.R.A.S Account creation","Your account has been created successfully. You can now upload your internship reports through the portal.",settings.EMAIL_HOST_USER,[clean_data["email"]],fail_silently=False,)
					user = serializer.check_user(clean_data)
					login(request, user)
					data_serializer = UserSerializer(user)
					return Response(data_serializer.data, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		if not validate_email(data): 
			return JsonResponse({'error':'An email is required'}, status=500)
		if not validate_password(data):
			return JsonResponse({'error':'A password is required'}, status=500)
		
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			if not user:
				return JsonResponse({'error':'Email or password are incorrect'}, status=500)

			login(request, user)
			data_serializer = UserSerializer(user)
			return Response(data_serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class PatchsView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		user = request.user
		if(user.type == 'Student'):
			return JsonResponse({'error':'You are not authorized'}, status=500)
		data = Patch.objects.all()
		serializer = PatchSerializer(data)
		return Response({'patches': serializer.data}, status=status.HTTP_200_OK)
	##
	def post(self, request):
		user = request.user
		if(user.type == 'Student'):
			return JsonResponse({'error':'You are not authorized'}, status=500)
		clean_data = validate_patch(request.data)
		print(clean_data)
		# return JsonResponse(clean_data, status=500)
		if "error" in clean_data.keys():
			return JsonResponse(clean_data, status=500)
		serializer = PatchSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			patch = serializer.create(clean_data)
			if patch:
				serializer = PatchSerializer(patch)
				return JsonResponse({'message': 'successully created patch','data':serializer.data}, status=status.HTTP_200_OK)
				
		return Response(status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	parser_classes = [MultiPartParser, FormParser]
	def post(self, request, format=None):
		user = request.user
		if(user.type == 'Admin'):
			return JsonResponse({'error':'You are not authorized'}, status=500)
		file_obj = request.FILES['file']
		print(request.user)
		# print(filename)
		print(format)
		print(file_obj)
		print(request.data)
        # do some stuff with uploaded file
		return Response(status=status.HTTP_200_OK)

