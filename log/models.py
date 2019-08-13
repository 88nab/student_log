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


#Created a custom user to ensure that the user_type would be included from the get-go
#This is beneficial for security aspects as different users will have access to different parts of the site
#As such, the username has to be unique as it will be used as a FK for many tables, 
#even though the email address could also be used as a PK
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

	def __str__(self):
		return self.username

#Using the package CustomUserField to aid the joining of my models due to issues encountered in previous attempts
#as a result of using a custom user rather than the default user. 
#This will make joining the database tables more streamlined, 
#as the current user field can effectively be used as part of the primary key in most tables
class Subject(models.Model):
	name = models.CharField(max_length=250, unique=True)
	views = models.IntegerField(default=0)
	likes=models.IntegerField(default=0)
	dislikes=models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	uploader = CurrentUserField()


	def save(self, *args, **kwargs):
		self.slug= slugify(self.name)
		super(Subject, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

#This model represents the videos uploaded by the lecturer. 
#Am currently using short videos as placeholders, 
#but will tell the users in testing to imagine they are lecture recordings
#Content uploaded by students will be detailed in other models.
class Video(models.Model):
	videoID = models.AutoField(primary_key=True)
	videoFile = models.FileField(upload_to='videos/', null=True, verbose_name="")
	videoDescription = models.CharField(max_length=250)
	upload_time = models.DateTimeField(default=timezone.now)
	uploader = CurrentUserField()
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	subject = models.ForeignKey(Subject)
	
	# Needed to convert this to a string - had issues getting the data from urls when it was an int
	# Was coming up as Video Object rather than the ID otherwise
	def __str__(self):
		return str(self.videoID)


# Not really ended up using this - might delete. 
#Easier to use username as user has to be logged in to access site anyway, 
#so there is no real need for a journal ID as well
class JournalCreator(models.Model):
	student = CurrentUserField()
	journalID = models.AutoField(primary_key=True)
	journal_name = models.CharField(max_length=50, unique=True)


#This is the content that a student uploads to their journal
#which will be accessible to other students. 
#Other students will be able to see how they have tagged the videos 
#and view them from the timestamp
class JournalContent(models.Model):
	student = CurrentUserField()
	videoID = models.ForeignKey(Video)
	time_saved = models.DateTimeField(default=timezone.now)
	timestamp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	#Looks as though it's defaulting to one decimal place, but there are two when you click on the  arrows
	#Need to fix it so that negative  numbers  aren't an option
	description = models.CharField(max_length=9999, null=True)
	tags = models.CharField(max_length=25)



#This is the content that a student uploads to their journal
#which will be private. It is, in effect, another way for them to save their notes -
#be it notes they took in a lecture, or additional notes they took after rewatching it,
#or indeed notes from having viewed other content uploaded by the students.
#There will be no way for other students to access this content.
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

	def snippet(self):
		return self.note[:25] + '...'


#This model represents files uploaded by students. Have used the file field,
#so they should be able to upload a wide variety of content.
#Will create another model so that the students can post comments and their responses
#to the uploads, so that they can discuss the content, perhaps providing each other with feedback, if necessary
class StudentFileUploads(models.Model):
	uploader = CurrentUserField()
	upload_file = models.FileField(upload_to='student-uploads/', null=True, verbose_name="")
	upload_file_id = models.AutoField(primary_key=True, default=0)#Created a default as I'd already populated the database before adding this field - will delete if I end up repopulating the database from scratch again
	subject = models.ForeignKey(Subject)
	upload_time = models.DateTimeField(default=timezone.now)
	tags = models.CharField(max_length=25)
	comment = models.TextField(max_length=9999, null=True)

	#I mistakenly included the s in the name of the class, so had to fix the verbose plural name
	class Meta:
		verbose_name_plural = 'Student File Uploads'

#Comment class for the file uploads
class FileComment(models.Model):
	first_post = models.ForeignKey(StudentFileUploads)
	author = CurrentUserField()
	comment = models.TextField(max_length=500)
	upload_time = models.DateTimeField(default=timezone.now)


#It is most unlikely that students would have access to their own video files to upload,
#so it made sense to include an opportunity to upload links to videos as well - 
#YouTube content that they might consider to be beneficial to the group. 
#Otherwise,  takes ont he same format as the model above
class StudentVideoLinkUploads(models.Model):
	uploader = CurrentUserField()
	upload_link = models.URLField(max_length=250)
	upload_link_id = models.AutoField(primary_key=True)
	subject = models.ForeignKey(Subject)
	upload_time = models.DateTimeField(default=timezone.now)
	tags = models.CharField(max_length=25)
	comment = models.CharField(max_length=9999, null=True)


	class Meta:
		verbose_name_plural = 'Student Link Uploads'

#Comment class for the link uploads
class LinkComment(models.Model):
	first_post = models.ForeignKey(StudentVideoLinkUploads)
	author = CurrentUserField()
	comment = models.TextField(max_length=500)
	upload_time = models.DateTimeField(default=timezone.now)



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




