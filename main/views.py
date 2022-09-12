from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date, parse_time
import datetime
from .models import *
from .utils import get_sidebar_info

#Logical Views

def add_todo(request):
    if request.method == "POST":
        parent_id = request.POST.get("parent")
        title = request.POST.get("title")
        description = request.POST.get("description")
        type = request.POST.get("type")
        new_todo = ToDo.objects.create()
        if parent_id == "None":
            if type == "calendar":
                date = request.POST.get('date')
                time = request.POST.get('time')
                date = parse_date(date)
                time = parse_time(time)
                date_time=datetime.datetime.combine(date, time)
            else:
                date_time = request.POST.get("date-time")
            priority = request.POST.get("priority")
            project_id = request.POST.get('project')
            if project_id != "None":
                project = Project.objects.filter(id=project_id).first()
                new_todo.project = project
            new_todo.title = title
            new_todo.description = description
            new_todo.date_time = date_time
            new_todo.author = request.user
            new_todo.priority = priority[-1]
        else:
            parent = ToDo.objects.filter(id=parent_id).first()
            new_todo.parent = parent
            new_todo.title = title
            new_todo.description = description
            new_todo.date_time = parent.date_time
            new_todo.author = parent.author
            new_todo.priority = parent.priority
            new_todo.project = parent.project
        new_todo.save()
        messages.success(request, "New Task has been successfully added!")
    return redirect(reverse('home_page'))

def signup_done(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            validate_password(password, user=username)
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            messages.success(request, "Your Edge Task account has been successfully created")
            login(request, new_user)
            personal = Project.objects.create(author=new_user, title="Personal")
            work = Project.objects.create(author=new_user, title="Work")
            education = Project.objects.create(author=new_user, title="Education")
            personal.save()
            work.save()
            education.save()
        except ValidationError as val_err:
            pass
    return redirect(reverse('home_page'))

def signing_up(request):
    if request.method == "POST":
        type = request.POST.get("type")
        if type == "password":
            password = request.POST.get("password")
            try:
                validate_password(password)
                data={"status": "success", "errors": []}
            except ValidationError as val_err:
                errors = []
                for err in val_err:
                    errors.append(err)
                data={"status": "error", "errors": errors}
        elif type == "username":
            username = request.POST['username']
            if User.objects.filter(username=username).exists():
                data = {'status': 'error', "message": "Username already exists!"}
            elif username == "":
                data = {'status': 'error', "message": "Username cannot be empty"}
            elif len(username) < 3:
                data = {'status': 'error', "message": "Username must be at least 3 characters"}
            elif len(username) > 16:
                data = {'status': 'error', "message": "Username must be less than 16 characters"}
            else:
                data = {'status': 'success', "message": "Username is available!"}

        else:
            data = {}
        return JsonResponse(data=data)
    return redirect(reverse('home_page'))

def handle_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!")
        else:
            return HttpResponse("No Matching User Found")
    return redirect(reverse('home_page'))

def handle_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Succcessfully Logged Out!") 
    return redirect(reverse('home_page'))

def task_view(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        task = ToDo.objects.filter(id=task_id).first()
        if task.project != None:
            allowed_users = task.project.allowed_users.all()
        else:
            allowed_users = []
        if request.user == task.author or request.user in allowed_users:
            comments = Comment.objects.filter(task=task)
            comment_array = []
            for comment in comments:
                comment_array.append({'author': comment.author.username, 'content': comment.content, 'date': comment.date})
            sub_tasks = ToDo.objects.filter(parent=task)
            sub_tasks_array = []
            for sub_task in sub_tasks:
                sub_tasks_array.append({'author': sub_task.author.username, 'title': sub_task.title, 'description': sub_task.description, 'date': sub_task.date_time, 'id': sub_task.id, 'done': sub_task.done})
            data = {'title': task.title, 'description': task.description, 'id': task.id, 'date': task.date_time, 'priority': task.priority, 'date_added': task.date_added, 'sub_tasks': sub_tasks_array, 'comments': comment_array}
            return JsonResponse(data=data)
        return HttpResponse("You are not allowed here!")
    return HttpResponse("Incorrect Method! Please try again.")

def delete_task(request):
    if request.method == "POST":
        task_id = request.POST.get("delete_task_id")
        task = ToDo.objects.filter(id=task_id).first()
        task.delete()
        messages.success(request, "Your Task has been deleted!")
    return redirect(reverse('home_page'))

def post_comment(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        task = ToDo.objects.filter(id=task_id).first()
        content = request.POST.get('content')
        comment = Comment.objects.create()
        comment.task = task
        comment.author = request.user
        comment.content = content
        comment.save()
        messages.success(request, "Comment Posted!")
    return redirect(reverse('home_page'))

def edit_task(request):
    if request.method == "POST":
        task_id = request.POST.get("task-id")
        task = ToDo.objects.filter(id=task_id).first()
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_time = request.POST.get('date-time')
        priority = request.POST.get("priority")
        task.title = title
        task.description = description
        task.date_time = date_time
        task.priority = priority[-1]
        task.save()
        messages.success(request, "Edited Task Successfully!")
    return redirect(reverse('home_page'))

def task_collab(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        reciever_username =  request.POST.get("reciever")
        project = Project.objects.filter(id=project_id).first()
        reciever = User.objects.filter(username=reciever_username).first()
        sender = request.user
        allowed_users = project.allowed_users.all()
        if sender == project.author and reciever not in allowed_users and reciever != project.author:
            invite = Invite.objects.create()
            invite.project = project
            invite.sender = sender
            invite.reciever = reciever
            invite.save()
            messages.success(request, f"Your invite has been sent successfully! {invite.reciever.username} will be added to the Project once they accept your Invite.")
    return redirect(reverse('home_page'))

def invite_view(request):
    if request.user.is_authenticated:
        user = request.user
        invites = Invite.objects.filter(reciever=user)

        counts, projects = get_sidebar_info(request)
        data = {"invites": invites, "projects": projects, "counts": counts}
        return render(request, 'main/invite.html', data)
    return redirect(reverse('home_page'))

def invite_form(request):
    if request.method == "POST":
        invite_id = request.POST.get("invite_id")
        invite = Invite.objects.get(id=invite_id)
        acceptance = request.POST.get("accept_and_reject")
        if acceptance == "Accept":
            project = invite.project
            project.allowed_users.add(invite.reciever)
            messages.success(request, f"You have been successfully added to the project {invite.project.title}!")
            project.save()
            invite.delete()
            return redirect(reverse('project', args=(project.slug,)))
        else:
            invite.delete()
    return redirect(reverse('home_page'))

def inbox_view(request):
    if request.user.is_authenticated:
        aware_datetime = make_aware(datetime.datetime.now())
        todo = ToDo.objects.filter((Q(author=request.user) | Q(project__allowed_users=request.user)), parent=None)
        delete_todos = todo.filter(done=True, date_done__gte=aware_datetime-datetime.timedelta(days=1)).all()
        for delete_todo in delete_todos:
            delete_todo.delete()
        counts, projects = get_sidebar_info(request)
        context = {"ToDo": todo, "heading": "Inbox", "counts": counts, "projects": projects, "is_project": False}
        return render(request, 'main/home.html', context)
    return render(request, 'main/signup.html')

def today_view(request):
    if request.user.is_authenticated:
        aware_datetime = make_aware(datetime.datetime.now())
        todo = ToDo.objects.filter(Q(author=request.user) | Q(project__allowed_users=request.user), parent=None, date_time__gte=aware_datetime-datetime.timedelta(days=1), date_time__lte=aware_datetime+datetime.timedelta(days=1))
        delete_todos = todo.filter(done=True, date_done__gte=aware_datetime-datetime.timedelta(days=1)).all()
        for delete_todo in delete_todos:
            delete_todo.delete()
        counts, projects = get_sidebar_info(request)
        context = {"ToDo": todo, "heading": "Today", "counts": counts, "projects": projects, "is_project": False}
        return render(request, 'main/home.html', context)
    return render(request, "main/signup.html")

def upcomming_view(request):
    if request.user.is_authenticated:
        aware_datetime = make_aware(datetime.datetime.now())
        todo = ToDo.objects.filter(Q(author=request.user) | Q(project__allowed_users=request.user), parent=None, date_time__gte=aware_datetime-datetime.timedelta(days=1), date_time__lte=aware_datetime+datetime.timedelta(days=7))
        delete_todos = todo.filter(done=True, date_done__gte=aware_datetime-datetime.timedelta(days=1)).all()
        for delete_todo in delete_todos:
            delete_todo.delete()
        counts, projects = get_sidebar_info(request)
        context = {"ToDo": todo, "heading": "Upcomming", "counts": counts, "projects": projects, "is_project": False}
        return render(request, 'main/home.html', context)
    return render(request, "main/signup.html")

def project_view(request, slug):
    project = Project.objects.filter(slug=slug).first()
    allowed_users = project.allowed_users.all()
    if request.user == project.author or request.user in allowed_users:
        aware_datetime = make_aware(datetime.datetime.now())
        todo = ToDo.objects.filter(project=project)
        
        counts, projects = get_sidebar_info(request)    
        context = {"ToDo": todo, "heading": project.title, "counts": counts, "project": project, "projects": projects, "allowed_users": allowed_users, "is_project": True}
        return render(request, 'main/home.html', context)
    else:
        return redirect(reverse('home_page'))

def new_project(request):
    if request.method == "POST":
        author = request.user
        title = request.POST.get('title')
        project = Project.objects.create(author=author, title=title)
        project.save()
        messages.success(request, "New Project Created!")
        return redirect(reverse('project', args=(project.slug,)))
    return redirect(reverse('home_page'))

def task_done(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        task = ToDo.objects.filter(id=task_id).first()
        if task.done:
            task.done = False
            task.date_done = make_aware(datetime.datetime.now())
        else:
            task.done = True
            task.date_done = None
        task.save()
        data = {"done": task.done, "priority": task.priority}
        return JsonResponse(data=data)
    return redirect(reverse('home_page'))

def calendar_view(request):
    return render(request, 'main/calendar.html')

def home_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('inbox'))
    return render(request, "main/get-started.html")

def calendar_view(request):
    if request.user.is_authenticated:
        user = request.user
        today = make_aware(datetime.datetime.today())
        projects = Project.objects.filter(allowed_users=user)
        tasks = ToDo.objects.filter(Q(author=user) | Q(project__in=projects), date_time__year=today.year)

        counts, projects = get_sidebar_info(request)
        data = {"tasks": tasks, "projects": projects, "counts": counts}
        return render(request, 'main/calendar.html', data)
    return redirect(reverse('home_page'))

def delete_project(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = Project.objects.filter(id=project_id).first()
        if request.user == project.author:
            project.delete()
            messages.success(request, "Project deleted Succesfully!")
    return redirect(reverse('home_page'))

def remove_project_user(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = Project.objects.get(id=project_id)
        if request.user == project.author:
            user_id = request.POST.get("user_id")
            user = User.objects.get(id=user_id)
            project.allowed_users.remove(user)
            project.save()
            messages.success(request, f"{user.username} got removed from the project {project.title} successfully!")
            return redirect(reverse('project', args=(project.slug,)))
    return redirect(reverse('home_page'))

def leave_project_user(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = Project.objects.get(id=project_id)
        project.allowed_users.remove(request.user)
        messages.success(request, f"You left the Project {project.title}")
    return redirect(reverse('home_page'))

def typing_project_username(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.filter(username=username)
        project_id = request.POST.get("project_id")
        project = Project.objects.filter(id=project_id).first()
        allowed_users = project.allowed_users.all()
        invite = Invite.objects.filter(sender=request.user, reciever=user.first(), project=project)
        
        if invite.exists():
            status = "error"
            message = "This Invite has already been sent!"
        else:
            if user.exists():
                if user.first() in allowed_users or user.first() == project.author:
                    status = "error"
                    message = "This user already exists in this Project!"
                else:
                    status = "success"
                    message = "User with this Username Exists!"
            else:
                status = "error"
                message = "No User found with this Username!"

        return JsonResponse(data={"status": status, "message": message})
    return redirect(reverse('home_page'))

#Rendering Views
def login_page(request):
    return render(request, "main/login.html")

def signup_page(request):
    return render(request, "main/signup.html")

