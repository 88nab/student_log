from django import forms
from django.contrib.auth.forms import UserCreationForm
from log.models import *


class CustomUserCreationForm(UserCreationForm):
	# email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('email', 'username', 'first_name', 'last_name', 'user_type')

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class UploadForm(forms.Form):
	video = forms.FileField(required=True)
	description = forms.CharField(widget=forms.Textarea)
	tags = forms.CharField(required=True)
	quiz = forms.CharField(required=True)
	