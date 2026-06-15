from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('check_email_exist', views.checkUsernameView.as_view(), name='check_email_exist'),
    path('me', views.UserInformation.as_view(), name="user_profile"),
    path('verify_email_phone', views.VerifyEmailPhone.as_view(), name='verify_email_phone'),
    path('change_password', views.ChangePassword.as_view(), name='change_password'),
    path("trimesters/", views.TrimesterListView.as_view(), name="trimester-list"),
    path("trimesters/<int:trimester_id>/", views.ExerciseListView.as_view(), name="trimester-list"),
    path("save_device_token/", views.SaveDeviceTokenView.as_view(), name="save_device_token"),
]
