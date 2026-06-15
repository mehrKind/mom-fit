from django.contrib import admin
from .models import UserProfile, Trimester, Exercise, ExerciseVideo, ExerciseSet, DeviceToken


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "full_name", "email", "phone_number",
        "is_pregnant", "after_pregnant",
        "week_of_pregnancy", "trimester_display"
    )
    list_filter = ("is_pregnant", "after_pregnant")
    search_fields = ("user__username", "full_name", "email", "phone_number")
    readonly_fields = ("trimester_display",)

    fieldsets = (
        ("User information", {
            "fields": ("user", "full_name", "email", "phone_number", "profile_picture")
        }),
        ("Pregnant information", {
            "fields": ("is_pregnant", "after_pregnant", "week_of_pregnancy", "trimester_display")
        }),
        ("More information", {
            "fields": ("bio", "age")
        }),
    )

    def trimester_display(self, obj):
        return obj.trimester()
    trimester_display.short_description = "3 of month"


@admin.register(Trimester)
class TrimesterAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "description")
    list_filter = ("number",)

class ExerciseVideoInline(admin.TabularInline):
    model = ExerciseVideo
    extra = 1  # تعداد فرم‌های خالی برای اضافه کردن ویدیو جدید
    show_change_link = True  # لینک به صفحه تغییر ویدیو

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "trimester")
    list_filter = ("trimester",)
    search_fields = ("name",)
    inlines = [ExerciseVideoInline]


@admin.register(ExerciseVideo)
class ExerciseVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "exercise", "order", "single")
    list_filter = ("exercise",)
    search_fields = ("title",)
    list_display_links = ("id", "title")
    list_editable = ("order", "single")


@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "number_of_reps", "duration_seconds", "rest_seconds")
    list_filter = ("video",)
    list_display_links = ("id", "video")


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "token")