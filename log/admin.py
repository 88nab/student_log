from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	model = CustomUser
	list_display = ['username', 'email', 'user_type']




admin.site.register(CustomUser)
# admin.site.register(CustomUserAdmin)
admin.site.register(Upload)
admin.site.register(QuizResult)
admin.site.register(Quiz)
admin.site.register(Forum)
admin.site.register(Journal)
admin.site.register(Video)
admin.site.register(Student)
admin.site.register(Subject)