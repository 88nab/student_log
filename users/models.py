from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your models here.

USER_TYPE_CHOICES = (
		('STUDENT', 'Student'),
		('LECTURER', 'Lecturer'),
	)

class CustomUser(AbstractUser):
	email = models.EmailField(max_length=70, unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='Student')
	username = models.CharField(max_length=20, unique=True)
	# password = forms.CharField(widget=forms.PasswordInput())