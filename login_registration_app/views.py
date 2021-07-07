from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            print(password_hash)
            user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = password_hash,
            )
            request.session['user_signed_in'] = user.id
            return redirect('/wall')

def wall(request):
    context = {
        'user_signed_in': User.objects.get(id=request.session['user_signed_in']),
        'all_messages': Message.objects.all()
    }
    return render(request,'wall.html', context)

def log_in(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            this_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_signed_in'] = this_user.id
                return redirect('/wall')    
        messages.error(request,"INCORRECT EMAIL / PASSWORD, OR UNREGISTERED USER ")
        return redirect('/')

def log_out(request):
    request.session.flush()
    return redirect('/')

def post_message(request):
    if request.method == 'POST':
        errors = Message.objects.basic_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/wall')
        else:
            Message.objects.create(
                message = request.POST['message'], 
                message_image = request.FILES.get('image'),
                user_posting = User.objects.get(id=request.session['user_signed_in'])
                )
            return redirect('/wall')
            
def post_comment(request, message_id):
    if request.method == 'POST':
        errors = Comment.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/wall')
        else:
            Comment.objects.create(
                comment=request.POST['comment'], 
                user_posting = User.objects.get(id=request.session['user_signed_in']),
                message = Message.objects.get(id=message_id),
                )
            return redirect('/wall')





