import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'student_log.settings')

import django
django.setup()
from log.models import *

# Commented this out for now - decided to change it from URLs to files

def populate():

	first_users = [
	{"email": "one@example.com",
	"first_name": "User",
	"last_name": "One",
	"user_type":"LECTURER",
	"username": "UserOne"
	},
	{"email": "two@example.com",
	"first_name": "User",
	"last_name": "Two",
	"user_type":"LECTURER",
	"username": "UserTwo"
	},
	{"email": "three@example.com",
	"first_name": "User",
	"last_name": "Three",
	"user_type":"STUDENT",
	"username": "UserThree"
	},
	{"email": "four@example.com",
	"first_name": "User",
	"last_name": "Four",
	"user_type":"STUDENT",
	"username": "UserFour"
	},

	]

	# first_subjects = [
	# {"name": "Cyber Security",
	# "views": 25,
	# "likes": 18,
	# "uploader": "UserOne",
	# },
	# {"name": "Software Engingeering",
	# "views": 45,
	# "likes": 32,
	# "uploader": "UserOne",
	# },
	# {"name": "Internet Technology",
	# "views": 30,
	# "likes": 25,
	# "uploader": "UserTwo",
	# },

	# ]

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


	for item in first_users:
		u = add_user(item["email"], item["first_name"], item["last_name"], item["user_type"], item["username"])
		print(format(str(u)))

	# for item in first_subjects:
	# 	s = add_subject(item["name"], item["views"], item["likes"], item["uploader"])

	# for item in first_videos:
	# 	v =

def add_user(email, first_name, last_name, user_type, username):
	uu, created = CustomUser.objects.get_or_create(email=email, first_name=first_name, last_name=last_name, user_type=user_type, username=username)
	uu.save()
	return uu

# def add_subject(name, views, likes, uploader):
# 	ss, created = Subject.objects.get_or_create(name=name, views=views, likes=likes, uploader=uploader)
# 	ss.save()
# 	return ss

# def add_video(videoID, videoFile, videoDescription, upload_time, uploader, views,  likes, subject):


if __name__ == '__main__':
	print("Starting log population script...") 
	populate()


