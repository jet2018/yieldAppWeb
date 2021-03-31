from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

admin.site.site_header = "YieldUp Admin"

class ProfileAdmin(admin.StackedInline):
	model= Profile
	list_display = ("role", "address", "bio", "years_of_experiance", "phone_number", "profile_pik")
	readonly_fields = ("user", "years_of_experiance", "phone_number", "stars")

class CustomUserAdmin(UserAdmin):
	inlines = (ProfileAdmin, )
	fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
	readonly_fields = ("email", "password",)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Profile, ProfileAdmin)
