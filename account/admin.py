from django.contrib import admin
from account.models import User
# Register your models here.

@admin.register(User)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ("user_id", 'username', 'email', 'profile_image')