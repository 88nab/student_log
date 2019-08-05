from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_currentuser.db.models import CurrentUserField
from django.template.defaultfilters import slugify

# Create your models here.

class CustomUser(AbstractUser):
	USER_TYPE_CHOICES = (
		('STUDENT', 'Student'),
		('LECTURER', 'Lecturer'),
	)
	email = models.EmailField(max_length=70, unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='Student')
	username = models.CharField(max_length=20, unique=True)

	# class Meta:
	# 	unique_together = (('email', 'user_type'))

	def __str__(self):
		return self.username


class Subject(models.Model):
	name = models.CharField(max_length=250, unique=True)
	views = models.IntegerField(default=0)
	likes=models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	uploader = CurrentUserField()


	def save(self, *args, **kwargs):
		self.slug= slugify(self.name)
		super(Subject, self).save(*args, **kwargs)

	def __str__(self):
		return self.name



# class Profile(models.Model):
# 	user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)

# @receiver(post_save,sender=CustomUser)
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		CustomUser.objects.created(user=instance)
# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance, **kwargs):
# 	instance.CustomUser.save()


# class StudentProfile(models.Model):
# 	profile=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

# class Subject(models.Model):
# 	lecturer = models.ForeignKey(CustomUser)
# 	name = models.CharField(max_length=128, blank=True) 
	# lecturer_email = CustomUser.objects.select_related('user_type').filter(user_type='LECTURER')
	
	# class Meta:
	# 	db_table = 'lecturer_user'

	# def __str__(self):
	# 	return self.lecturer

class Video(models.Model):
	videoID = models.AutoField(primary_key=True)
	videoFile = models.FileField(upload_to='videos/', null=True, verbose_name="")
	videoDescription = models.CharField(max_length=250)
	upload_time = models.DateTimeField(default=timezone.now)
	uploader = CurrentUserField()
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	subject = models.ForeignKey(Subject)
	
	def __str__(self):
		return str(self.videoID)

class JournalCreator(models.Model):
	student = CurrentUserField()
	journalID = models.AutoField(primary_key=True)
	journal_name = models.CharField(max_length=50, unique=True)


class JournalContent(models.Model):
	student = CurrentUserField()
	videoID = models.ForeignKey(Video)
	time_saved = models.DateTimeField(default=timezone.now)
	timestamp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	description = models.CharField(max_length=9999, null=True)
	tags = models.CharField(max_length=25)




class Comment(models.Model):
	video = models.ForeignKey(Video)
	user = CurrentUserField()
	def __unicode__(self):
		return self.name
	comment = models.CharField(max_length=2000, null=True)
	date_posted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.comment

class Note(models.Model):
	student = CurrentUserField()
	subject = models.ForeignKey(Subject)
	title = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(unique=True)
	created_on = models.DateTimeField(default=timezone.now)
	note = models.TextField()



	def save(self, *args, **kwargs):
		self.slug= slugify(self.title)
		super(Note, self).save(*args, **kwargs)

	def __str__(self):
		return self.title




		

	# def save_model(self, request, obj, form, change):
	# 	obj.added_by = request.user
	# 	super().save_model(request, obj, form, change)

	# def __str__(self):
	# 	return self.videoID + ":" + str(self.videoFile)

# class Journal(models.Model):
# 	# student= models.ForeignKey(Student)
# 	videoID = models.ForeignKey(Video)
# 	journalID = models.AutoField(primary_key=True)
# 	time_saved = models.DateTimeField(default=timezone.now)
# 	timestamp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
# 	description = models.CharField(max_length=9999, null=True)

# class Student(models.Model):
# 	student = models.OneToOneField(CustomUser)
# 	# student_email = CustomUser.objects.select_related('user_type').filter(user_type='STUDENT')
# 	journalID = models.ForeignKey(Journal)
	
	# class Meta:
	# 	db_table = 'student_user'

	# def __str__(self):
	# 	return self.student

# class Video(models.Model):
# 	videoID = models.AutoField(primary_key=True)
# 	videoDescription = models.CharField(max_length=250)
# 	videoFile = models.FileField(upload_to='videos/', null=True, verbose_name="")
# 	views = models.IntegerField(default=0)
# 	likes = models.IntegerField(default=0)

# 	def __str__(self):
# 		return self.videoID + ":" + str(self.videoFile)

# class Journal(models.Model):
# 	# student= models.ForeignKey(Student)
# 	videoID = models.ForeignKey(Video)
# 	journalID = models.AutoField(primary_key=True)
# 	time_saved = models.DateTimeField(default=timezone.now)
# 	timestamp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
# 	description = models.CharField(max_length=9999, null=True)

# class Forum(models.Model):
# 	videoID = models.ForeignKey(Video)
# 	author_email = models.ForeignKey(Student)
# 	time_posted = models.DateTimeField(default=timezone.now)
# 	comment = models.CharField(max_length=5000, null=True)


# class Quiz(models.Model):
# 	quizID = models.AutoField(primary_key=True)
# 	# quiz_questions =
# 	# quiz_answers = 

# 	class Meta:
# 		verbose_name_plural = 'Quizzes'

# 	def __str__(self):
# 		return self.quizID


# class QuizResult(models.Model):
# 	quizID = models.ForeignKey(Quiz)
# 	studentID = models.ForeignKey(Student)
# 	time_taken = models.DateTimeField(default=timezone.now)
# 	result = models.IntegerField(default=0)



# class Upload(models.Model):
# 	# videoID = models.ForeignKey(Video)
# 	# lecturer_email = models.ForeignKey(Subject)
# 	# quizID = models.ForeignKey(Quiz)
# 	upload_time = models.DateTimeField(default=timezone.now)
# 	description = models.CharField(max_length=9999, null=True)
# 	tag = models.CharField(max_length=25)


