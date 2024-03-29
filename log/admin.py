from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from log.forms import CustomUserCreationForm, CustomUserChangeForm
from log.models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
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

class StudentFileUploadsAdmin(admin.ModelAdmin):
	list_display=('uploader', 'upload_file', 'upload_time')

class StudentVideoLinkUploadsAdmin(admin.ModelAdmin):
	list_display=('uploader', 'upload_link', 'upload_time')

class FileCommentAdmin(admin.ModelAdmin):
	list_display=('first_post', 'author', 'comment')

class LinkCommentAdmin(admin.ModelAdmin):
	list_display=('first_post', 'author', 'comment')

class QuizAdmin(admin.ModelAdmin):
	list_display=('quizID', 'quiz_name', 'video')

class QuestionAdmin(admin.ModelAdmin):
	list_display=('question', 'quiz', 'correct_answer')



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(JournalCreator, JournalCreatorAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(JournalContent, JournalContentAdmin)
admin.site.register(StudentFileUploads, StudentFileUploadsAdmin)
admin.site.register(StudentVideoLinkUploads, StudentVideoLinkUploadsAdmin)
admin.site.register(FileComment, FileCommentAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)




