from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from main.models import Patch,Submissions

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
			patch = Patch.objects.create(semester=clean_data['semester'],close_date=clean_data['close_date'],start_date=clean_data['start_date'],open=False)
			patch.save()
			return patch
		else:
			patch = Patch.objects.create(semester=clean_data['semester'],close_date=clean_data['close_date'])
			patch.save()
			return patch
	
# class PatchCreationsSerializer(serializers.ModelSerializer):
# 	semester = serializers.CharField(max_length=50)
# 	close_date = serializers.DateField()
# 	def create(self, clean_data):
# 		patch = Patch.objects.create(semester=clean_data['semester'])
# 		patch.save()
# 		return patch

class SubmissionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Submissions
		fields = '__all__'