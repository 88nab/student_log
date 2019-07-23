from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.utils import timezone

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

	# class Meta:
	# 	unique_together = (('email', 'user_type'))

	def __str__(self):
		return self.user_type

class Subject(models.Model):
	name = models.CharField(max_length=128) 
	# Not suure if I need to define the subject
	lecturer_email = CustomUser.objects.select_related('user_type').filter(user_type='Lecturer')

class Student(models.Model):
	student_email = CustomUser.objects.select_related('user_type').filter(user_type='Student')
	journalID = models.AutoField(primary_key=True)

class Video(models.Model):
	videoID = models.AutoField(primary_key=True)
	videoDescription = models.CharField(max_length=250, default="xxx")
	videoFile = models.FileField(upload_to='videos/', null=True, verbose_name="")
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

	def __str__(self):
		return self.videoID + ":" + str(self.videoFile)

class Journal(models.Model):
	student= models.ForeignKey(Student)
	videoID = models.ForeignKey(Video)
	# journalID
	time_saved = models.DateTimeField(default=timezone.now)
	timestamp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	description = models.CharField(max_length=9999, null=True)

class Forum(models.Model):
	videoID = models.ForeignKey(Video)
	author_email = models.ForeignKey(Student)
	time_posted = models.DateTimeField(default=timezone.now)
	comment = models.CharField(max_length=5000, null=True)


class Quiz(models.Model):
	quizID = models.AutoField(primary_key=True)
	# quiz_questions =
	# quiz_answers = 

	class Meta:
		verbose_name_plural = 'Quizzes'

	def __str__(self):
		return self.quizID


class QuizResult(models.Model):
	quizID = models.ForeignKey(Quiz)
	studentID = models.ForeignKey(Student)
	time_taken = models.DateTimeField(default=timezone.now)
	result = models.IntegerField(default=0)



class Upload(models.Model):
	videoID = models.ForeignKey(Video)
	lecturer_email = models.ForeignKey(Subject)
	quizID = models.ForeignKey(Quiz)
	upload_time = models.DateTimeField(default=timezone.now)
	description = models.CharField(max_length=9999, null=True)
	tag = models.CharField(max_length=25)


