

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




	