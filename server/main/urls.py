from django.urls import path
from . import views

urlpatterns = [
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
	path('upload', views.FileUploadView.as_view(), name='upload'),
	path('patch', views.PatchsView.as_view(), name='patch'),
	path('patch/<int:patch_id>/<str:action>', views.PatchView.as_view(), name='patch'),
	path('student-submission', views.StudentSubmissionsView.as_view(), name='submission'),
    path('student-patch', views.StudentPatchView.as_view(), name='student-patch')
]
