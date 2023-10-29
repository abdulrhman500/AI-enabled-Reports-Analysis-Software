from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, PatchSerializer, SubmissionsSerializer, AdminSubmissionsSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password, validate_patch, validate_sub_data
from main.models import AppUser,Patch,Submissions
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os
from rest_framework.parsers import FileUploadParser,MultiPartParser, FormParser
import datetime
from pytz import timezone

def handle_uploaded_file(file,patch):
	file_name = file.name
	if not os.path.exists(r'uploads/'+patch.semester):
		os.makedirs(r'uploads/'+patch.semester)
	with open(r'uploads/'+patch.semester+'/'+file_name, "wb+") as destination:
		for chunk in file.chunks():
			destination.write(chunk)

def delete_file(file_name, patch):
	if os.path.exists(r'uploads/'+patch.semester+'/'+file_name):
		os.remove(r'uploads/'+patch.semester+'/'+file_name)

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
		serializer = PatchSerializer(data, many = True)
		return Response({'data': serializer.data}, status=status.HTTP_200_OK)
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

class PatchView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request, patch_id, action):
		if action == 'data':
			user = request.user
			if(user.type == 'Student'):
				return JsonResponse({'error':'You are not authorized'}, status=500)
			if not Patch.objects.filter(id = patch_id).exists():
				return JsonResponse({'error':'No such patch'}, status=500)
			patch = Patch.objects.get( id=patch_id)
			patch_serializer = PatchSerializer(patch)
			submissions = Submissions.objects.filter(patch=patch)
			submissions_serializer = AdminSubmissionsSerializer(submissions, many = True)
			return Response({'patch': patch_serializer.data, 'submissions': submissions_serializer.data}, status=status.HTTP_200_OK)
		return JsonResponse({'error':'You are not authorized'}, status=500)
	##
	def post(self, request, patch_id, action):
		user = request.user
		if(user.type == 'Student'):
			return JsonResponse({'error':'You are not authorized'}, status=500)
		if not Patch.objects.filter(id = patch_id).exists():
				return JsonResponse({'error':'No such patch'}, status=500)
		
		patch = Patch.objects.get( id=patch_id)
		if action == 'save':
			if patch.open:
				return JsonResponse({'error':"Patch is still open. Patchs must be closed in order to finalize it's results."}, status=500)
			if patch.start_date > datetime.datetime.now(timezone('UTC')).astimezone(timezone('Africa/Cairo')):
				return JsonResponse({'error':"Patch has not open yet. Finalizing a patch that was never open will result in an empty patch."}, status=500)
			patch.processed = True
			patch.save()
			return Response({'message':'Patch finalized successfully.'}, status=status.HTTP_200_OK)
		
		if action == 'delete':
			if patch.open:
				return JsonResponse({'error':"Patch is still open. Patchs can not be deleted once opened."}, status=500)
			if patch.start_date < datetime.datetime.now(timezone('UTC')).astimezone(timezone('Africa/Cairo')):
				return JsonResponse({'error':"Patch can not be deleted. Patchs can not be deleted once opened."}, status=500)
			patch.delete()
			return Response({'message':'Patch deleted successfully.'}, status=status.HTTP_200_OK)
		if action == 'close':
			if patch.open:
				patch.open = False
				patch.save()
				return Response({'message':'Patch closed successfully.'}, status=status.HTTP_200_OK)
			else:
				return JsonResponse({'error':"Patch is not open. Patchs must be open to be closed."}, status=500)
		if action == 'resume':
			if not patch.open:
				if patch.start_date > datetime.datetime.now(timezone('UTC')).astimezone(timezone('Africa/Cairo')):
					return JsonResponse({'error':"Patch is not open yet. Patchs can not be started ahead of schedual."}, status=500)
				if patch.close_date < datetime.datetime.now(timezone('UTC')).astimezone(timezone('Africa/Cairo')):
					return JsonResponse({'error':"Patch duration ended. Patchs can not be resumed past duration."}, status=500)
				patch.open = True
				patch.save()
				return Response({'message':'Patch resumed successfully.'}, status=status.HTTP_200_OK)
			else:
				return JsonResponse({'error':"Patch is not closed. Patchs must be closed to be opened."}, status=500)
		
		if action == 'update':
			clean_data = validate_sub_data(request.data)
			subs = Submissions.objects.filter(id__in = clean_data['sub_ids'])
			for sub in subs:
				print(clean_data['verdict'])
				sub.verdict =  clean_data['verdict']
				sub.note =  clean_data['note']
				sub.save()
			return Response({'message':'Submissions updated successfully.'}, status=status.HTTP_200_OK)
		
		return Response(status=status.HTTP_400_BAD_REQUEST)

class StudentPatchView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	def get(self, request):
		patch = Patch.objects.get(open = True)
		uploaded_once = False
		if Submissions.objects.filter(patch = patch, student = request.user).exists():
			uploaded_once = True
		if patch:
				serializer = PatchSerializer(patch)
				return JsonResponse({'message': 'successully created patch','data':serializer.data,'uploaded':uploaded_once}, status=status.HTTP_200_OK)
		return JsonResponse({'error':'No patch found'}, status=500)

class StudentSubmissionsView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	parser_classes = [MultiPartParser, FormParser]

	def post(self, request, format=None):
		print(request.path)
		user = request.user
		if(user.type == 'Admin'):
			return JsonResponse({'error':'You are not authorized'}, status=500)
		file_obj = request.FILES['file']
		patch = Patch.objects.get(open=True)
		if not patch:
			return JsonResponse({'error':'No open patches are available'}, status=500)
		handle_uploaded_file(file_obj, patch)
		serializer = SubmissionsSerializer()
		if Submissions.objects.filter(patch=patch, student = request.user).exists():
			previous = Submissions.objects.get(patch=patch, student = request.user)
			delete_file(previous.file_upload, patch)
			previous.file_upload = file_obj.name
			upload_date = datetime.datetime.now(timezone('UTC'))
			upload_date = upload_date.astimezone(timezone('Africa/Cairo'))
			previous.upload_date = upload_date
			previous.save()
			return JsonResponse({'message': 'Report submitted successfully'}, status=status.HTTP_200_OK)
		submission = serializer.create(student = user, patch = patch, file_name = file_obj.name)
		if submission:
			return JsonResponse({'message': 'Report submitted successfully'}, status=status.HTTP_200_OK)
			
		return Response(status=status.HTTP_400_BAD_REQUEST)
	
	def get(self, request):
		submissions = Submissions.objects.filter(student=request.user)
		if submissions:
				serializer = SubmissionsSerializer(submissions, many=True)
				return JsonResponse({'data':serializer.data}, status=status.HTTP_200_OK)
		return JsonResponse({'data':{}}, status=status.HTTP_200_OK)

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
		print(file_obj.name)
		print(request.data)
		handle_uploaded_file(file_obj)
        # do some stuff with uploaded file
		return Response(status=status.HTTP_200_OK)
