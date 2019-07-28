# from django import template
# from log.models import Subject


# register = template.Library()

# @register.inclusion_tag('log/subject.html', takes_context=True)
# def get_subject_list(context):
# 	request = context['request']
# 	current_user= request.user.username
# 	user_subject = Subject.objects.order_by(Subject.name).filter(uploader=current_user)
# 	return {'user_subject': user_subject}