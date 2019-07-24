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
	context_dict = {'user_type': user_type}
	response = render(request, 'log/index.html', context=context_dict)
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
			
			return redirect('index') 
		else: 
			print(form.errors)

	context_dict = {'form':form}

	return render(request, 'log/registration_form.html', context_dict)

def contact_us(request):
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
	return render(request, "log/contact_us.html", {'form': form})

# Need to fix this
def successView(request):
	return HttpResponse('Success! Thank you for your message.')

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('change_password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'log/change_password.html', {
		'form': form
	})

@login_required
def user_logout(request):
	logout(request)
	return render(request, 'log/logout.html', context={})

def upload(request):
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('index')
	else:
		form = UploadForm()  
	return render(request, 'log/upload.html', {'form': form})









