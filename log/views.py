import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from log.forms import *
from log.models import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime


@login_required 
def index(request):
	# Have to add the user_type and subjects to every view so that the complete dropdown menu
	# appears in the navbar - perhaps a quicker way to fix this would be to create a view for the base.
	# Will look into tidying it later, focusing on getting more functionality first
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	most_viewed=Video.objects.all().order_by('-views')[:5]
	response = render(request, 'log/index.html', {'videos': most_viewed,'user_type': user_type, 'subjects':subjects})
	return response

def user_login(request):
	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Student's Log account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied. Please return to the previous page and re-enter your details to log in.")
	else:
		return render(request, 'log/login.html', {})

def register_profile(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST, request.FILES) 
		if form.is_valid(): 
			user_profile = form.save(commit=False) 
			user_profile.user = request.user 
			user_profile.save()
			print(user_profile.user_type)
			messages.info(request, "Thank you for registering with Student's Log. You are now logged in.")
			user_profile = authenticate(username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				user_type=form.cleaned_data['user_type'],)
			login(request, user_profile)
			if user_profile.user_type=='STUDENT':
				return redirect('journal_creator') 
			else:
				return redirect('add_subject')
		else: 
			print(form.errors)

	context_dict = {'form':form}

	return render(request, 'log/registration_form.html', context_dict)

def contact_us(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')

	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			
			subject = form.cleaned_data['subject']
			email = form.cleaned_data['email']
			message = form.cleaned_data['message']

			send_mail(subject+" - " + email, message, email, ['catchhub1@gmail.com'])
			return redirect('index')
	return render(request, "log/contact_us.html", {'form': form, 'user_type': user_type, 'subjects':subjects})

# Not currently using this
def successView(request):
	return HttpResponse('Success! Thank you for creating a quiz.')

@login_required 
def change_password(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user) 
			messages.success(request, 'Your password was successfully updated!')
			return redirect('index')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'log/change_password.html', {
		'form': form, 'user_type': user_type, 'subjects':subjects
	})

@login_required 
def profile(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	response = render(request, 'log/profile.html', {'user_type': user_type, 'subjects':subjects})
	return response

@login_required 
def edit_profile(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	

	if request.method=='POST':
		form = CustomUserChangeForm(request.POST, instance=request.user)
		if form.is_valid:
			form.save()
			return redirect('profile')
	else:
		form = CustomUserChangeForm(instance=request.user)
		context_dict= {'form': form, 'user_type': user_type, 'subjects':subjects}

	response = render(request, 'log/edit_profile.html', context_dict)
	return response

@login_required
def user_logout(request):
	logout(request)
	return render(request, 'log/logout.html', context={})

@login_required 
def upload(request, subject_name_slug):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	try:
		subject= Subject.objects.get(slug=subject_name_slug)
		current_user = request.user.username
		subject_details = Subject.objects.values('uploader')
	except Subject.DoesNotExist:
		subject = None

	form = UploadForm()
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			if subject:
				video=form.save(commit=False)
				# video.uploader = request.user
				# Going to try and change from using current user field after I next delete the database
				video.subject=subject
				video.views=0
				video.likes=0
				video.save()
			return show_subject(request, subject_name_slug)
	else:
		print(form.errors) 
	context_dict={'form': form, 'subject': subject, 'user_type': user_type, 'subjects':subjects}
	return render(request, 'log/upload.html', context_dict)

@login_required 
def add_subject(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	form = SubjectForm()
	if request.method == 'POST':
		form = SubjectForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print(form.errors)

	return render(request, 'log/add_subject.html', {'form': form, 'user_type': user_type, 'subjects':subjects})

@login_required 
def show_subject(request, subject_name_slug):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')	
	context_dict = {}

	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		if subject:
			views= subject.views + 1
			subject.views =views
			subject.save()
			# Views will go up if it's viewed by a lecturer or a student

		videos = Video.objects.filter(subject=subject)
		IDs = videos.values('videoID')
		tags = JournalContent.objects.filter(videoID=IDs)
		views = subject.views
		context_dict['videos'] = videos
		context_dict['tags'] = tags
		context_dict['subject'] = subject
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Subject.DoesNotExist:
		context_dict['videos'] = None
		context_dict['subject'] = None
		context_dict['tags'] = None
	return render(request, 'log/subject.html', context_dict)

@login_required 
def journal_creator(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	form = JournalCreatorForm()
	if request.method == 'POST':
		form = JournalCreatorForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print(form.errors)

	return render(request, 'log/journal_creator.html', {'form': form, 'user_type': user_type, 'subjects':subjects})

@login_required 
def forum_view(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	response = render(request, 'log/forum.html', {'user_type': user_type, 'subjects':subjects})
	return response


def like_video(request):
	videoID =None
	if request.method=='GET':
		videoID= request.GET['videoID']
	likes=0
	if videoID:
		video=Video.objects.get(videoID=videoID)
		if video:
			likes= video.likes + 1
			video.likes =likes
			video.save()
		return HttpResponse(likes)

def like_subject(request):
	slug =None
	if request.method=='GET':
		slug= request.GET['slug']
	likes=0
	if slug:
		slug=Subject.objects.get(slug=slug)
		if slug:
			likes= slug.likes + 1
			slug.likes =likes
			slug.save()
		return HttpResponse(likes)


def dislike_video(request):
	videoID =None
	if request.method=='GET':
		videoID= request.GET['videoID']
	dislikes=0
	if videoID:
		video=Video.objects.get(videoID=videoID)
		if video:
			dislikes= video.dislikes + 1
			video.dislikes =dislikes
			video.save()
		return HttpResponse(dislikes)


def dislike_subject(request):
	slug =None
	if request.method=='GET':
		slug= request.GET['slug']
	likes=0
	if slug:
		slug=Subject.objects.get(slug=slug)
		if slug:
			dislikes= slug.dislikes + 1
			slug.dislikes =dislikes
			slug.save()
		return HttpResponse(dislikes)

@login_required 
def video_stats(request, videoID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict={}

	try:
		video = Video.objects.get(videoID=videoID)
		tags = JournalContent.objects.filter(videoID=videoID)
		context_dict['video']= video
		context_dict['tags'] = tags
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Video.DoesNotExist:
		context_dict['video']= None
		context_dict['tags'] = None

	response = render(request, 'log/stats.html', context_dict)
	return response

@login_required 
def video_test(request, videoID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict={}

	try:
		video = Video.objects.get(videoID=videoID)
		if video:
			views= video.views + 1
			video.views =views
			video.save()
			# More tracking hits rather than actual views - will improve in further releases
			# The views, however, are limited to student hits to the page
		context_dict['video']= video
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Video.DoesNotExist:
		context_dict['video']= None

	response = render(request, 'log/video_test.html', context_dict)
	return response

@login_required 
def show_journal(request, username):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	notes = Note.objects.filter(student=request.user).order_by('-created_on')
	timestamps = JournalContent.objects.filter(student=request.user)
	context_dict={'notes':notes, 'timestamps': timestamps, 'user_type':user_type, 'subjects': subjects, 'username': username}

	return render(request, 'log/journal.html', context_dict)

@login_required 
def add_note(request, username):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	form = NoteForm()
	if request.method == 'POST':
		form = NoteForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print(form.errors)

	context_dict={'form': form, 'user_type':user_type, 'subjects': subjects, 'username': username,}
	return render(request, 'log/note_form.html', context_dict)

@login_required 
def show_note(request, slug):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict={}

	try:
		note = Note.objects.get(slug=slug)
		context_dict['note']= note
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Video.DoesNotExist:
		context_dict['note']= None

	response = render(request, 'log/note.html', context_dict)
	return response

@login_required 
def add_journal_content(request, videoID):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	video = Video.objects.get(videoID=videoID)
	form = JournalContentForm()
	if request.method == 'POST':
		form = JournalContentForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print(form.errors)

	context_dict={'form': form, 'user_type':user_type, 'subjects': subjects, 'video': video,}
	return render(request, 'log/journal_content_form.html', context_dict)

@login_required 
def video_tags(request, videoID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	tags = JournalContent.objects.filter(videoID=videoID)
	context_dict = {'tags': tags, 'user_type':user_type, 'subjects': subjects,}
	response = render(request, 'log/tags.html', context_dict)
	return response

@login_required 
def search_tags(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	tags = JournalContent.objects.all().order_by('tags') #Tags from journal
	sTags = StudentFileUploads.objects.all().order_by('tags') #Tags from student uploads
	sLinks = StudentVideoLinkUploads.objects.all().order_by('tags') #Tags from student link uploads
	response = render(request, 'log/search_tags.html', {'tags':tags, 'sTags':sTags, 'sLinks':sLinks, 'user_type': user_type, 'subjects':subjects})
	return response

@login_required 
def subject_discussion(request, subject_name_slug):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict = {}

	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		uploads = StudentFileUploads.objects.filter(subject=subject).order_by('-upload_time')
		links = StudentVideoLinkUploads.objects.filter(subject=subject).order_by('-upload_time')
		context_dict['subject'] = subject
		context_dict['uploads']= uploads
		context_dict['links']= links
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Subject.DoesNotExist:
		context_dict['subject'] = None
		context_dict['uploads'] = None
		context_dict['links'] = None
	return render(request, 'log/subject-discussion.html', context_dict)


@login_required 
def add_subject_file(request, subject_name_slug):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	subject = Subject.objects.get(slug=subject_name_slug)
	user = request.user
	form = StudentFileUploadsForm()
	if request.method == 'POST':
		form = StudentFileUploadsForm(request.POST, request.FILES)
		if form.is_valid():
			if subject:
				file=form.save(commit=False)
				file.subject=subject
				file.uploader = user
				file.save()
			return subject_discussion(request, subject_name_slug)
	else:
		print(form.errors) 

	context_dict={'form': form, 'user_type':user_type, 'subjects': subjects, 'subject':subject, 'user': user,}
	return render(request, 'log/student-file-upload.html', context_dict)

@login_required 
def add_subject_link(request, subject_name_slug):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	subject = Subject.objects.get(slug=subject_name_slug)
	user = request.user
	form = StudentVideoLinkUploadsForm()
	if request.method == 'POST':
		form = StudentVideoLinkUploadsForm(request.POST, request.FILES)
		if form.is_valid():
			if subject:
				link=form.save(commit=False)
				link.subject=subject
				link.uploader = user
				link.save()
			return subject_discussion(request, subject_name_slug)
	else:
		print(form.errors) 

	context_dict={'form': form, 'user_type':user_type, 'subjects': subjects, 'subject':subject, 'user': user,}
	return render(request, 'log/student-link-upload.html', context_dict)

@login_required 
def view_file_discussion(request, subject_name_slug, fileID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	first_post = StudentFileUploads.objects.get(upload_file_id=fileID)
	comments = FileComment.objects.filter(first_post=first_post).order_by('upload_time')
	context_dict={}
	form = FileCommentForm()
	if request.method == 'POST':
		form = FileCommentForm(request.POST)

		if form.is_valid():
			comment = request.POST.get('comment') 
			comment =FileComment.objects.create(first_post=first_post, author=request.user, comment=comment)
			comment.save()
			return HttpResponseRedirect(request.path_info)

		else:
			form = FileCommentForm()

	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		file = StudentFileUploads.objects.get(upload_file_id=fileID)
		context_dict['subject']= subject
		context_dict['file']= file
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
		context_dict['comments']= comments
		context_dict['form']=form
	except StudentFileUploads.DoesNotExist:
		context_dict['file']= None

	response = render(request, 'log/file-discussion.html', context_dict)
	return response

@login_required 
def timestamped_video(request, videoID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict={}

	try:
		journal_item = JournalContent.objects.get(videoID=videoID)
		print(journal_item.timestamp)
		video = Video.objects.get(videoID=videoID)
		if video:
			views= video.views + 1
			video.views =views
			video.save()
			# Like above - just counting actual views of the page rather than interaction with video
			# Would need to develop further in future releases
		context_dict['journal_item']= journal_item
		context_dict['video']= video
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except JournalContent.DoesNotExist:
		context_dict['journal_item']= None
		context_dict['video']= None

	response = render(request, 'log/timestamped-video.html', context_dict)
	return response

@login_required 
def view_link_discussion(request, subject_name_slug, linkID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	first_post = StudentVideoLinkUploads.objects.get(upload_link_id=linkID)
	comments = LinkComment.objects.filter(first_post=first_post).order_by('upload_time')
	context_dict={}
	form = FileCommentForm()
	if request.method == 'POST':
		form = FileCommentForm(request.POST)

		if form.is_valid():
			comment = request.POST.get('comment') 
			comment =LinkComment.objects.create(first_post=first_post, author=request.user, comment=comment)
			comment.save()
			return HttpResponseRedirect(request.path_info)

		else:
			form = FileCommentForm()

	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		link = StudentVideoLinkUploads.objects.get(upload_link_id=linkID)
		context_dict['subject']= subject
		context_dict['link']= link
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
		context_dict['comments']= comments
		context_dict['form']=form
	except StudentFileUploads.DoesNotExist:
		context_dict['link']= None

	response = render(request, 'log/link-discussion.html', context_dict)
	return response

@login_required 
def view_video_link(request, subject_name_slug, linkID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	link = StudentVideoLinkUploads.objects.get(upload_link_id=linkID)
	subject = Subject.objects.get(slug=subject_name_slug)
	
	context_dict ={'link': link,  'subject': subject, 'user_type':user_type, 'subjects': subjects,}

	return render(request, 'log/embedded-link.html', context_dict)

@login_required 
def add_quiz(request, subject_name_slug, videoID):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	subject = Subject.objects.get(slug=subject_name_slug)
	video = Video.objects.get(videoID=videoID)
	form = QuizForm()
	context_dict={'form': form, 'user_type':user_type, 'subjects': subjects, 'video': video,}
	if request.method == 'POST':
		form = QuizForm(request.POST)

		if form.is_valid():
			quiz = request.POST.get('quiz_name') 
			quiz =Quiz.objects.create(quiz_name=quiz, creator=request.user, video=video, subject = subject)
			quiz.save()
			return redirect('add_question', quizID=quiz.quizID)

		else:
			print(form.errors)

	return render(request, 'log/add_quiz.html', context_dict)


@login_required 
def add_question(request, quizID):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	quiz = Quiz.objects.get(quizID=quizID)
	form = QuestionForm()
	context_dict={'form': form, 'user_type':user_type, 'subjects': subjects, 'quiz': quiz,}
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			question  =  request.POST.get('question')
			first_answer=request.POST.get('first_answer')
			second_answer=request.POST.get('second_answer')
			third_answer=request.POST.get('third_answer')
			fourth_answer=request.POST.get('fourth_answer')
			correct_answer=request.POST.get('correct_answer')
			question = Question.objects.create(question=question, first_answer=first_answer, second_answer=second_answer, third_answer=third_answer, fourth_answer=fourth_answer, correct_answer=correct_answer, quiz=quiz)
			question.save()

		else:
			print(form.errors)

	return render(request, 'log/add_question.html', context_dict)


