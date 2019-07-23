import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'student_log.settings')

import django
django.setup()
from log.models import *

# Commented this out for now - decided to change it from URLs to files

# def populate():

# 	test_videos = [
# 	{"videoID": "https://www.youtube.com/watch?v=UmljXZIypDc",
# 	"views":23,
# 	"likes":18
# 	 },
# 	{"videoID": "https://www.youtube.com/watch?v=D6esTdOLXh4",
# 	"views":45,
# 	"likes":23
# 	 },
# 	 {"videoID": "https://www.youtube.com/watch?v=qDwdMDQ8oX4",
# 	"views":9,
# 	"likes":3
# 	 },
# 	 {"videoID": "https://www.youtube.com/watch?v=SIyxjRJ8VNY",
# 	"views":32,
# 	"likes":22
# 	 },
# 	 {"videoID": "https://www.youtube.com/watch?v=UyQn0BhVqNU",
# 	"views":12,
# 	"likes":8
# 	 },
# 	 {"videoID": "https://www.youtube.com/watch?v=M9rtf7icuG0",
# 	"views":18,
# 	"likes":5
# 	 },

# 	]


# 	for item in test_videos:
# 		v= add_video(item["videoID"], item["views"], item["likes"])
# 		print(format(str(v)))


# def add_video(videoID, views=0, likes=0):
# 	vv = Video.objects.get_or_create(videoID=videoID, views=views, likes=likes)[0]
# 	vv.save()
# 	return vv


# if __name__ == '__main__':
# 	print("Starting log population script...") 
# 	populate()