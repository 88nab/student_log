# Don't actually think I need all of these 
#as I've been able to achieve what I want putting stuff in views.
#As such, I only registered subjects in the settings.py.
#Have added the other ones in as I go in case I do encounter difficulties,
#but it is unlikely that I will need them

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
	comments = Comment.objects.all()

	return {
		'comments': comments,
	}
def notes(request):
	from log.models import Note
	notes = Note.objects.all()

	return {
		'notes': notes,
	}

def timestamps(request):
	from log.models import JournalContent
	timestamps= JournalContent.objects.all()

	return {
		'timestamps':timestamps,
	}

def studentUploads(request):
	from log.models import StudentFileUploads
	uploads= StudentFileUploads.objects.all()

	return {
		'uploads':uploads,
	}



	