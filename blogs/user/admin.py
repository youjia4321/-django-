from django.contrib import admin
from user.models import UserProfile, EmailCodeRecord, MessageModel
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "gender", "mobile")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailCodeRecord)
admin.site.register(MessageModel)