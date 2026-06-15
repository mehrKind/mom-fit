from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_pregnant = models.BooleanField(default=True)
    after_pregnant = models.BooleanField(default=False)
    # حذف month_of_pregnancy و فقط استفاده از هفته
    week_of_pregnancy = models.IntegerField(default=0)
    age = models.IntegerField(default=0)

    @property
    def month_of_pregnancy(self):
        """محاسبه ماه از هفته به صورت داینامیک"""
        if not self.is_pregnant or self.week_of_pregnancy <= 0:
            return 0
        
        # محاسبه دقیق‌تر بر اساس استاندارد پزشکی
        week_to_month = [
            (4, 1), (8, 2), (13, 3), (17, 4), (21, 5),
            (26, 6), (30, 7), (35, 8), (40, 9)
        ]
        
        for week, month in week_to_month:
            if self.week_of_pregnancy <= week:
                return month
        return 9

    def trimester(self):
        """بر اساس هفته بارداری، سه‌ماهه رو برمی‌گردونه"""
        if 1 <= self.week_of_pregnancy <= 13:
            return 1
        elif 14 <= self.week_of_pregnancy <= 26:
            return 2
        elif 27 <= self.week_of_pregnancy <= 40:
            return 3
        return 0


    def __str__(self):
        return f"Profile of {self.user.username}"


class Trimester(models.Model):
    number = models.IntegerField(choices=[(1, "اول"), (2, "دوم"), (3, "سوم")])
    description = models.TextField(blank=True)

    def __str__(self):
        return f"سه‌ماهه {self.number}"


class Exercise(models.Model):
    trimester = models.ForeignKey(Trimester, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.trimester}"


class ExerciseVideo(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='exercise_videos/')
    order = models.PositiveIntegerField(default=0)
    single = models.BooleanField(default=False)  # آیا این ست تکی است یا بخشی از یک مجموعه
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.exercise.name})"


class ExerciseSet(models.Model):
    video = models.ForeignKey(ExerciseVideo, on_delete=models.CASCADE, related_name="sets")
    number_of_reps = models.IntegerField(default=0)  # تعداد تکرار در هر ست
    duration_seconds = models.IntegerField(default=0)  # مدت زمان (ثانیه)
    rest_seconds = models.IntegerField(default=0)  # استراحت بین ست‌ها (اختیاری)


    def __str__(self):
        return f"ست {self.id} از {self.video.title}"


class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device_tokens")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
