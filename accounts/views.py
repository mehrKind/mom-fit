from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from random import randint
from mom_fit.settings import sms_ir
# from .notification import send_notification

from .models import UserProfile, Trimester, Exercise, DeviceToken
from .serializers import (
    UserProfileSerializer, TrimesterSerializer,
    ExerciseSerializer, UserSerializer
)


# DEVICE_TOKEN = DEVICE_TOKEN = "fVVgWNEpRNKwtQ9LC8Xivj:APA91bF76wMckoOUg66qNCq18rgEPAZIGpw1L_-mi_D8pQQUVtD0DXOmRHfeVQvAsQZjK8OTWcU00H11DLp_jMZ-fZ4XhHm46zx6BBV99jjDb7-jLqeuExc"

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
#             return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.create_user(
#             username=data['username'],
#             email=data['email'],
#             password=data['password']
#         )

#         UserProfile.objects.create(
#             user=user,
#             bio="New user profile",
#             full_name=data['fullName'],
#             email=data['email'],
#             phone_number=data['phoneNumber'],
#             week_of_pregnancy=data["week_of_pregnancy"]

#         )

#         refresh = RefreshToken.for_user(user)
#         # send notif after register
#         send_notification(
#             device_token=DEVICE_TOKEN,
#             title="Welcome to MoM Fit",
#             body="Thank you for registering!",
#         )
#         return Response({
#             'user': UserSerializer(user).data,
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         }, status=status.HTTP_201_CREATED)


class checkUsernameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        phone_number = data.get('phone_number')
        if (not email) or (not phone_number):
            return Response({'error': 'user is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if UserProfile.objects.filter(phone_number=phone_number).exists() or UserProfile.objects.filter(email=email).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'exists': False}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
        #     return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        UserProfile.objects.create(
            user=user,
            bio="New user profile",
            full_name=data['fullName'],
            email=data['email'],
            phone_number=data['phoneNumber'],
            week_of_pregnancy=data["week_of_pregnancy"]
        )

        # device_token = data.get("device_token")
        # if device_token:
        #     DeviceToken.objects.get_or_create(user=user, token=device_token)

        refresh = RefreshToken.for_user(user)
        print(data['phoneNumber'])
        sms_ir.send_sms(
            data['phoneNumber'],
            f"{data['fullName']} عزیز، به دنیای امکانات MoM Fit خوش اومدی! ",
            "30002101007292"
        )
        print("SMS sent successfully.")

        # if device_token:
        #     send_notification(
        #         device_token=device_token,
        #         title="Welcome to MoM Fit",
        #         body="Thank you for registering!",
        #     )

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(email=data['email'])
            if user.check_password(data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        return Response({'error': 'کاربر وجود ندارد'}, status=status.HTTP_401_UNAUTHORIZED)


class UserInformation(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            profile = request.user.profile
            print(f"✅ Profile found: {profile}")
        except UserProfile.DoesNotExist:
            print("❌ Profile not found!")
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"❌ Other error getting profile: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print("✅ Successfully got profile")
        serializer = UserProfileSerializer(profile)
        return Response({
            "status": 200,
            "data": serializer.data,
            "error": None
        })

    def patch(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "error": None
            })
        return Response({
            "status": 400,
            "data": None,
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# verify email and phone number
class VerifyEmailPhone(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        random_number = randint(1000, 9999)

        if "email" in data:
            try:
                validators.validate_email(data['email'])
                profile = UserProfile.objects.filter(
                    email=data['email']).first()
                if not profile:
                    return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

                request.session['random_number'] = str(random_number)
                request.session['email'] = data['email']
                request.session.save()

                send_mail(
                    subject="Email Verification",
                    message="Your validation code is below",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[data['email']],
                    html_message=f"<html><body><p>Code: <strong>{random_number}</strong></p></body></html>",
                    fail_silently=False,
                )

                return Response({"status": 200, "data": f"Code sent: {random_number}"})

            except ValidationError:
                return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        elif "phoneNumber" in data:
            profile = UserProfile.objects.filter(
                phone_number=data['phoneNumber']).first()
            if not profile:
                return Response({"error": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)

            request.session['random_number'] = str(random_number)
            request.session['phoneNumber'] = data['phoneNumber']
            request.session.save()
            try:
                sms_ir.send_sms(
                    data['phoneNumber'],
                    f"کد تایید شما: {random_number} ",
                    "30002101007292"
                )
            except Exception as e:
                print(f"Error sending SMS: {e}")

            return Response({"status": 200, "data": f"Code sent: {random_number}"})

        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        digit_code = request.data.get('code')
        if 'random_number' in request.session and str(digit_code) == request.session['random_number']:
            request.session.flush()
            return Response({"status": 200, "data": "Verification successful"})

        return Response({"error": "Code mismatch or missing"}, status=400)


class ChangePassword(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        new_password = request.data.get("password")
        way_id = request.data.get("way_id")

        if not new_password or not way_id:
            return Response({"error": "Missing password or way_id"}, status=400)

        user = User.objects.filter(email=way_id).first()
        if not user:
            profile = UserProfile.objects.filter(phone_number=way_id).first()
            if profile:
                user = profile.user

        if not user:
            return Response({"error": "User not found"}, status=404)

        user.set_password(new_password)
        user.save()

        return Response({"status": 200, "data": "Password changed successfully"})


# class UserProfileView(APIView):
#     """نمایش پروفایل کاربر"""

#     def get(self, request, user_id):
#         user_profile = get_object_or_404(UserProfile, user__id=user_id)
#         serializer = UserProfileSerializer(user_profile)
#         context = {
#             "status": 200,
#             "data": serializer.data,
#             "error": ""
#         }
#         return Response(context, status=status.HTTP_200_OK)


class TrimesterListView(APIView):
    """list of trimesters and its exercises"""

    def get(self, request):
        trimesters = Trimester.objects.all()
        serializer = TrimesterSerializer(trimesters, many=True)
        context = {
            "status": 200,
            "data": serializer.data,
            "error": ""
        }
        return Response(context, status=status.HTTP_200_OK)


class ExerciseListView(APIView):
    """List of exercises for a specific trimester, including trimester description"""

    def get(self, request, trimester_id):
        trimester = get_object_or_404(Trimester, number=trimester_id)
        # serialize the whole trimester
        serializer = TrimesterSerializer(trimester)
        context = {
            "status": 200,
            "data": serializer.data,
            "error": ""
        }
        return Response(context, status=status.HTTP_200_OK)


class SaveDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Save or update the device token
        device_token, created = DeviceToken.objects.get_or_create(
            user=request.user, token=token)

        if created:
            message = "Device token saved successfully"
        else:
            message = "Device token already exists"

        return Response({"status": 200, "data": message}, status=status.HTTP_200_OK)

    def put(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the device token
        device_token = DeviceToken.objects.filter(user=request.user).first()
        if device_token:
            device_token.token = token
            device_token.save()
            return Response({"status": 200, "data": "Device token updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Device token not found"}, status=status.HTTP_404_NOT_FOUND)
