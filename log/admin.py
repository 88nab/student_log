from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from log.forms import CustomUserCreationForm
from log.models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	model = CustomUser
	list_display = ['username', 'email', 'user_type']

class StudentAdmin(admin.ModelAdmin):
	list_display= ('student', 'journalID')

class VideoAdmin(admin.ModelAdmin):
	list_display=('videoID', 'videoFile', 'uploader', 'subject')

class SubjectAdmin(admin.ModelAdmin):
	list_display=('name', 'uploader')

class JournalCreatorAdmin(admin.ModelAdmin):
	list_display=('journalID', 'student')

class NoteAdmin(admin.ModelAdmin):
	list_display=('student', 'title')

class JournalContentAdmin(admin.ModelAdmin):
	list_display=('student','videoID', 'timestamp')



admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Upload)
# admin.site.register(QuizResult)
# admin.site.register(Quiz)
# admin.site.register(Forum)
# admin.site.register(Journal)
admin.site.register(Video, VideoAdmin)
# admin.site.register(Student, StudentAdmin)
# admin.site.register(StudentProfile)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(JournalCreator, JournalCreatorAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(JournalContent, JournalContentAdmin)