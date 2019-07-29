

def subjects(request):
	from log.models import Subject 
	subs = Subject.objects.all()

	return {
		'subs': subs,
	}

def videos(request):
	from log.models import Video 
	vids = Video.objects.all()

	return {
		'vids': vids,
	}	

def comments(request):
	from log.models import Comment 
	vids = Comment.objects.all()

	return {
		'comments': comments,
	}