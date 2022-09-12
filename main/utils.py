from .models import *
from django.db.models import Q
from django.utils.timezone import make_aware

def get_sidebar_info(request):
    today = make_aware(datetime.datetime.today())
    today_count = ToDo.objects.filter(Q(author=request.user) | Q(project__allowed_users=request.user), parent=None, date_time__gte=today-datetime.timedelta(days=1), date_time__lte=today+datetime.timedelta(days=1)).count()
    inbox_count = ToDo.objects.filter(Q(author=request.user) | Q(project__allowed_users=request.user), parent=None).count()
    upcomming_count = ToDo.objects.filter(Q(author=request.user) | Q(project__allowed_users=request.user), parent=None, date_time__gte=today-datetime.timedelta(days=1), date_time__lte=today+datetime.timedelta(days=7)).count()
    invite_count = Invite.objects.filter(reciever=request.user).count()
    projects = Project.objects.filter(Q(author=request.user) | Q(allowed_users=request.user)).distinct()
    counts = {"inbox_count": inbox_count, "today_count": today_count, "upcomming_count": upcomming_count, "invite_count": invite_count}
    return counts, projects
