from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, PatchSerializer, SubmissionsSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password, validate_semester
from main.models import AppUser,Patch,Submissions
from django.http import JsonResponse

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
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
		data = Patch.objects.all()
		serializer = PatchSerializer(data)
		return Response({'patches': serializer.data}, status=status.HTTP_200_OK)
	##
	def post(self, request):
		clean_data = validate_semester(request.data)
		serializer = PatchSerializer(data=clean_data)
		return Response({'patch': serializer.data}, status=status.HTTP_200_OK)

