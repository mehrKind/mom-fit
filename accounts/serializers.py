# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Trimester, Exercise, ExerciseVideo, ExerciseSet
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']


# class UserProfileSerializer(serializers.ModelSerializer):
#     trimester = serializers.SerializerMethodField()

#     class Meta:
#         model = UserProfile
#         fields = '__all__'  # includes all model fields
#         extra_fields = ['trimester']  # optional, for documentation

#     def get_trimester(self, obj):
#         """Returns which trimester the user is in based on month_of_pregnancy."""
#         month = obj.month_of_pregnancy
#         if month == 0:
#             return "0"
#         elif 1 <= month <= 3:
#             return "1"
#         elif 4 <= month <= 6:
#             return "2"
#         elif 7 <= month <= 9:
#             return "3"
#         else:
#             return "Invalid month"


class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ["id", "number_of_reps","duration_seconds", "rest_seconds"]


class ExerciseVideoSerializer(serializers.ModelSerializer):
    sets = ExerciseSetSerializer(many=True, read_only=True)

    class Meta:
        model = ExerciseVideo
        fields = ["id", "title", "video_file","single", "order", "sets"]
        


class ExerciseSerializer(serializers.ModelSerializer):
    videos = ExerciseVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ["id", "name", "description", "videos"]


class TrimesterSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Trimester
        fields = ["id", "number", "description", "exercises"]


class UserProfileSerializer(serializers.ModelSerializer):
    trimester = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id", "user", "full_name", "email", "phone_number", "date_joined",
            "profile_picture", "bio", "is_pregnant", "after_pregnant",
            "month_of_pregnancy", "week_of_pregnancy", "age", "trimester"
        ]

    def get_trimester(self, obj):
        return obj.trimester()
    
    def get_date_joined(self, obj):
        return obj.user.date_joined.date() if obj.user.date_joined else None
