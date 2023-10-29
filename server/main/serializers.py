from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from main.models import Patch,Submissions
import datetime
from pytz import timezone

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'],username = clean_data['username'],user_id=clean_data['user_id'] )
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			return False
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username', 'type')

class PatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patch
		fields = '__all__'

	def create(self, clean_data):
		if 'start_date' in clean_data.keys():
			start_date = datetime.datetime.strptime(clean_data['start_date'], '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
			start_date=start_date.astimezone(timezone('Africa/Cairo'))
			close_date = datetime.datetime.strptime(clean_data['close_date'], '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
			close_date=close_date.astimezone(timezone('Africa/Cairo'))
			patch = Patch.objects.create(semester=clean_data['semester'],close_date=close_date,start_date=start_date,open=False)
			patch.save()
			return patch
		else:
			close_date = datetime.datetime.strptime(clean_data['close_date'], '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
			close_date=close_date.astimezone(timezone('Africa/Cairo'))
			patch = Patch.objects.create(semester=clean_data['semester'],close_date=close_date)
			patch.save()
			return patch

class SubmissionsSerializer(serializers.ModelSerializer):
	patch = PatchSerializer(read_only=True)
	class Meta:
		model = Submissions
		fields = '__all__'
	def create(self, student, patch, file_name):
		submission = Submissions.objects.create(student = student, file_upload = file_name, patch = patch)
		submission.save()
		return submission

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('username', 'user_id')


class AdminSubmissionsSerializer(serializers.ModelSerializer):
	student = StudentSerializer(read_only=True)
	class Meta:
		model = Submissions
		fields = '__all__'