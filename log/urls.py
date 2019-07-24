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
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^add_subject/$', views.add_subject, name='add_subject'),
    # url(r'^subject/(?P<subject_name_slug>[\w\-]+)/$', views.show_subject, name='show_category'),
	# url(r'^subject/(?P<subject_name_slug>[\w\-]+)/add_quiz/$', views.add_quiz, name='add_quiz'),

]
