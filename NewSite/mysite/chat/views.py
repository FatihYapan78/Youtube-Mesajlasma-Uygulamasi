from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def index(request):
    users = User.objects.all().exclude(username=request.user)
    
    return render(request, "chat/index.html",{
        'users':users,
    })

@login_required(login_url="login")
def room(request, room_name):
    users = User.objects.all().exclude(username=request.user)
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)

    if request.user != room.first_user:
        if request.user != room.second_user:
            return redirect('index')

    return render(request, "chat/room2.html", {
        "room_name": room_name,
        'users':users,
        'room':room,
        'messages':messages,
        })

@login_required(login_url="login")
def video(request, room_name):
    room = Room.objects.get(id=room_name)
    if request.user != room.first_user:
        if request.user != room.second_user:
            return redirect('index')
    return render(request, 'chat/video_chat.html',{'room':room})

@login_required(login_url="login")
def start_chat(request,username):
    second_user = User.objects.get(username=username)
    try:
        room = Room.objects.get(first_user=request.user,second_user=second_user)
        # first_user = fatih
        # second_user = faruk

        # first_user = faruk
        # second_user = fatih
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user,first_user=second_user)
        except:
            Room.objects.create(first_user=request.user,second_user=second_user)
    return redirect("room",room.id)

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return redirect("Login")
    
    return render(request, "chat/login.html")
