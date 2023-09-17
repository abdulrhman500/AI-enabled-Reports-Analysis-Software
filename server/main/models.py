from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import time
import datetime

def get_date():
	return datetime.datetime.now()

def upload_to(instance, filename):
	current_time_millis = str(int(round(time.time() * 1000)))
	return 'uploads/{filename}{current_time_millis}'.format(filename=filename)

# Create your models here.
class AppUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, user_id=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		if user_id:
			user = self.model(pk=user_id,email=email,username=username)
			user.set_password(password)
			user.save()
			return user
		else:
			user = self.model(email=email,username=username)
			user.set_password(password)
			user.save()
			return user
		
	def create_superuser(self, email, username, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email=email, password=password,username=username)
		user.is_superuser = True
		user.is_staff = True
		user.type = "Admin"
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50)
	TYPES = [('Admin', "Admin"),('Student', "Student")]
	type = models.CharField(choices = TYPES, default = 'Student')
	USERNAME_FIELD = 'email'
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()
	def __str__(self):
		return self.username
	

class Patch(models.Model):
	semester = models.CharField(max_length=50)
	processed = models.BooleanField(default = False)
	open = models.BooleanField(default = True)
	created_at = models.DateTimeField(auto_now_add = True)
	start_date = models.DateTimeField(default=get_date)
	close_date = models.DateTimeField()
	REQUIRED_FIELDS = ['close_date','semester']
	def __str__(self):
		return self.semester

	

class Submissions(models.Model):
	name = models.CharField(max_length=50)
	registeration_id = models.ForeignKey(AppUser, on_delete = models.CASCADE)
	file_upload = models.FileField(upload_to=upload_to)
	judgement = models.BooleanField(default = False)
	created_at = models.DateTimeField(auto_now_add = True)
	patch = models.ForeignKey(Patch, on_delete = models.CASCADE)
	REQUIRED_FIELDS = ['file_upload','name']
	def __str__(self):
		return self.file_upload