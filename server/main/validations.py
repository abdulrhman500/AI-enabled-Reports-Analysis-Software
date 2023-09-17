from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from main.models import Patch,Submissions
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    user_id = data['user_id']
    ##
    if not user_id:
        return {"error":'Student id is required'}
    ##
    if not email:
        return {"error":'An email is required'}
    ##
    if UserModel.objects.filter(email=email).exists():
        return {"error":'This email is already registered'}
    ##
    if UserModel.objects.filter(user_id=user_id).exists():
        return {"error":'This student id is already registered'}
    ##
    if not password or len(password) < 8:
        return {"error":'choose another password, min 8 characters'}
    ##
    if not username:
        return {"error":'A user name is required'}
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        return False
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        return False
    return True

def validate_patch(data):
    semester = data['semester'].strip()
    close_date = data['close_date'].strip()
    start_data = None
    if 'start_date' in data.keys():
        start_data = data['start_date'].strip()
    if not semester:
        return {"error":'Semester is required'}
    if not close_date:
        return {"error":'Close date is required'}
    if not start_data and Patch.objects.filter(open=True).exists():
        return {"error":'A patch is already open'}
    return data