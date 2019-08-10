from django.conf.urls import url 
from log import views
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^add_subject/$', views.add_subject, name='add_subject'),
    url(r'^subject/(?P<subject_name_slug>[\w\-]+)/$', views.show_subject, name='show_subject'),
    url(r'^subject/(?P<subject_name_slug>[\w\-]+)/upload/$', views.upload, name='upload'),
	# url(r'^subject/(?P<subject_name_slug>[\w\-]+)/add_quiz/$', views.add_quiz, name='add_quiz'),
    url(r'^journal_creator/$', views.journal_creator, name='journal_creator'),
    # url(r'^subject/(?P<subject_name_slug>[\w\-]+)/video/(?P<videoID>\d+)/$', views.show_video, name='show_video'),
    url(r'^forum/$', views.forum_view, name='forum_view'),
    url(r'^stats/video/(?P<videoID>\d+)/$', views.video_stats, name='video_stats'),
    url(r'^viewer/video/(?P<videoID>\d+)/$', views.video_test, name='video_test'),
    url(r'^(?P<username>[\w\-]+)/journal/$', views.show_journal, name='show_journal'),
    url(r'^(?P<username>[\w\-]+)/journal/add_note/$', views.add_note, name='add_note'),
    url(r'^journal/view_note/(?P<slug>[\w\-]+)/$', views.show_note, name='show_note'),
    url(r'^(?P<videoID>\d+)/journal/save_timecodes/$', views.add_journal_content, name='add_journal_content'),
    url(r'^video/(?P<videoID>\d+)/tags/$', views.video_tags, name='video_tags'),
    url(r'^search_tags/$', views.search_tags, name='search_tags'),
    url(r'^like/$', views.like_video, name='like_video'),
    url(r'^like-subject/$', views.like_subject, name='like_subject'),
    url(r'^dislike/$', views.dislike_video, name='dislike_video'),
    url(r'^dislike-subject/$', views.dislike_subject, name='dislike_subject'),
    url(r'^subject/(?P<subject_name_slug>[\w\-]+)/subject-discussion/$', views.subject_discussion, name='subject_discussion'),
    url(r'^subject/(?P<subject_name_slug>[\w\-]+)/file-upload/$', views.add_subject_file, name='add_subject_file'),
]
