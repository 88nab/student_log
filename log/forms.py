from django import forms
from django.contrib.auth.forms import UserCreationForm
from log.models import *


class CustomUserCreationForm(UserCreationForm):
	# email = forms.EmailField(required=True)
	# password = forms.CharField(widget=forms.PasswordInput())

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('email', 'username', 'first_name', 'last_name', 'user_type')

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class UploadForm(forms.ModelForm):
	# video = forms.FileField(required=True)
	# lecturer_email =
	# description = forms.CharField(widget=forms.Textarea)
	# tags = forms.CharField(required=True)
	# quiz = forms.CharField(required=True)
	

	class Meta:
		model = Video
		exclude = ('videoID', 'uploader', 'upload_time','views', 'likes', 'subject')

	# def save(self):
	# 	video = self.cleaned_data['video']
	# 	description = self.cleaned_data['description']
	# 	tags = self.cleaned_data['tags']
	# 	quiz = self.cleaned_data['quiz']
	
class SubjectForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the name of your subject.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model = Subject
		fields = ('name',)


	