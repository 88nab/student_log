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


@login_required 
def index(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	most_viewed=Video.objects.all().order_by('-views')[:5]
	# most_liked=Video.objects.all().order_by('-likes')[:5]
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

# Need to fix this
def successView(request):
	return HttpResponse('Success! Thank you for your message.')

def change_password(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
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
def user_logout(request):
	logout(request)
	return render(request, 'log/logout.html', context={})

def upload(request, subject_name_slug):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	try:
		subject= Subject.objects.get(slug=subject_name_slug)
		current_user = request.user.username
		subject_details = Subject.objects.values('uploader')
		# print (current_user.)
		# print (subject_details.query)
		# if subject_details != current_user:
		# 	return HttpResponse('You cannot upload content to this subject. Please select one of your own subjects.')
	except Subject.DoesNotExist:
		subject = None

	form = UploadForm()
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			if subject:
				video=form.save(commit=False)
				video.subject=subject
				video.views=0
				video.save()
			return show_subject(request, subject_name_slug)
	else:
		print(form.errors) 
	context_dict={'form': form, 'subject': subject, 'user_type': user_type, 'subjects':subjects}
	return render(request, 'log/upload.html', context_dict)

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

def show_subject(request, subject_name_slug):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')	
	context_dict = {}

	try:
		subject = Subject.objects.get(slug=subject_name_slug)
		videos = Video.objects.filter(subject=subject)
		context_dict['videos'] = videos
		context_dict['subject'] = subject
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Subject.DoesNotExist:
		context_dict['videos'] = None
		context_dict['subject'] = None
	return render(request, 'log/subject.html', context_dict)


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

# def show_video(request, subject_name_slug, videoID):
# 		context_dict = {}
# 		user_type = CustomUser.objects.values('user_type')
# 		subjects = Subject.objects.all().order_by('uploader')
# 		subject = Subject.objects.get(slug=subject_name_slug)
# 		videos = Video.objects.get(videoID=videoID)
# 		selected_video = videos.videoID
# 		print(subject)
# 		print(videos.videoID)


# 		# selected_subject = Subject.objects.filter(subject_name_slug).order_by(videoID=selected_video)
# 		# subject_name_slug = request.GET['slug']
# 		# videoID = request.GET['videoID']
# 		# selected_subject = request.GET.get('slug', None)
# 		# selected_video = request.GET.get('videoID', None)
# 		# video_detail = None
# 		# video_id_integer = int(videoID)
		
# 		# vid_list = Video.objects.filter(videoID=video_id_integer)

# 		# if len(vid_list) > 0:
# 		# 	video_detail = vid_list[0]
# 		# else:
# 		# 	video_detail = None

# 		try:
# 			# subject = Subject.objects.get(slug=subject_name_slug)
# 			# videos = Video.objects.get(videoID=videoID)
# 			comment = Comment.objects.filter(videoID=videoID).order_by('-date_posted')
# 			form = CommentForm()
# 			context_dict['comment'] =  comment

# 			if request.method == 'POST':
# 				form.videos = videos
# 				form = CommentForm(request.POST)

# 				if form.is_valid():
# 					getInfo = form.save(commit=False)
# 					getInfo.save()

# 					info_dict = {"comment": getInfo.comment, "date": getInfo.date_posted.strftime('%B %d, %Y, %I:%M %p')}
# 					return HttpResponse(json.dumps(info_dict), content_type="application/json",)

# 				else:
# 					print(form.errors)

# 		except Subject.DoesNotExist:
# 			context_dict['videos'] = None
# 			context_dict['comment'] = None

# 		context_dict = {'form': form,'selected_video': selected_video, 'comment':comment, 'user_type': user_type, 'subjects':subjects}
# 		print(videoID)
# 		xxx = int(videoID)
# 		print(xxx)
# 		# try:
# 		# 	subject = Subject.objects.get(slug=subject_name_slug)
# 		# 	videos = Video.objects.get(videoID=videoID)
# 		# 	# context_dict= {'subject': subject, 'videos':videos, 'user_type': user_type, 'subjects': subjects}
# 		# 	context_dict['subject'] = subject
# 		# 	context_dict['videos'] = videos
# 		# 	context_dict['user_type']=user_type
# 		# 	context_dict['subjects']= subjects
# 		# except Subject.DoesNotExist:
# 		# 	context_dict['videos'] = None
# 		# 	context_dict['subject'] = None
# 		return render(request, 'log/video.html', context_dict)

def forum_view(request):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	response = render(request, 'log/forum.html', {'user_type': user_type, 'subjects':subjects})
	return response

# def like_video(request):
# 	videoID =None
# 	if request.method=='GET':
# 		videoID= request.GET['videoID']
# 	likes=0
# 	if videoID:
# 		video=Video.objects.get(id=int(videoID))
# 		if video:
# 			likes= video.likes + 1
# 			video.likes =likes
# 			video.save()
# 		return HttpResponse(likes)

def video_stats(request, videoID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict={}

	try:
		video = Video.objects.get(videoID=videoID)
		context_dict['video']= video
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Video.DoesNotExist:
		context_dict['video']= None

	response = render(request, 'log/stats.html', context_dict)
	return response


def video_test(request, videoID):
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	context_dict={}

	try:
		video = Video.objects.get(videoID=videoID)
		context_dict['video']= video
		context_dict['user_type']=user_type
		context_dict['subjects']= subjects
	except Video.DoesNotExist:
		context_dict['video']= None

	response = render(request, 'log/video_test.html', context_dict)
	return response



# def show_video(request, videoID, subject_name_slug):
# 	user_type = CustomUser.objects.values('user_type')
# 	subjects = Subject.objects.all().order_by('uploader')
# 	context_dict={}

# 	print(isinstance(videoID, str))
# 	vid_as_int = int(videoID)
# 	print(isinstance(vid_as_int, int))
# 	try:
# 		video = Video.objects.get(videoID=vid_as_int)
# 		subject = Subject.objects.get(slug=subject_name_slug)
# 		context_dict['video']= video
# 		context_dict['subject'] = subject
# 		context_dict['user_type']=user_type
# 		context_dict['subjects']= subjects
# 	except Video.DoesNotExist:
# 		context_dict['video']= None
# 		context_dict['subject']= None

# 	response = render(request, 'log/video.html', context_dict)
# 	return response

def show_video(request, subject_name_slug, videoID):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	# video = Video.objects.get(videoID=videoID)
	# subject = Subject.objects.get(slug=subject_name_slug)
	print(videoID)
	print(subject_name_slug)
	context_dict={'user_type':user_type, 'subjects': subjects, 'videoID':videoID, 'subject_name_slug':subject_name_slug}
	# print(video)
	
	# try:
	# 	context_dict['video']= video
	# 	context_dict['subject']  = subject
	# 	context_dict['user_type']=user_type
	# 	context_dict['subjects']= subjects
	# except Video.DoesNotExist:
	# 	context_dict['video']= None
	
	return render(request, 'log/video.html', context_dict)

def show_journal(request, username):
	context_dict={}
	user_type = CustomUser.objects.values('user_type')
	subjects = Subject.objects.all().order_by('uploader')
	notes = Note.objects.filter(student=request.user)
	context_dict={'notes':notes, 'user_type':user_type, 'subjects': subjects, 'username': username}

	return render(request, 'log/journal.html', context_dict)

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


