from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    con_delete = False # 프로필 아예 삭제 불가

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username')
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)