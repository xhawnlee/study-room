from django.shortcuts import render,redirect
from .models import Room,Topic,Message,User
# Create your views here.
from .forms import RoomForm,UserForm,MyRegisterUserForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
# 自带user
# from django.contrib.auth.models import User
# 自带user的注册
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
  # rooms = Room.objects.all().order_by('-created')
  search_selected = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=search_selected) |
    Q(name__icontains = search_selected) |
    Q(host__username__icontains = search_selected)
  ).order_by('-created')
  total_room = Room.objects.all().count
  room_count = rooms.count
  topics = Topic.objects.all()
  msgs = Message.objects.all().order_by('-created')
  # user_rooms = user.room_set.all().count

  context = {'rooms':rooms,'topics':topics,'msgs':msgs,'room_count':room_count,'total_room':total_room}
  return render(request,'base/home.html',context)

def room(request,pk):
  room = Room.objects.get(id=pk)
  msgs = room.message_set.all().order_by('-created')
  participants = room.participants.all()
  if request.method == 'POST':
    Message.objects.create(
      user = request.user,
      room = room,
      content = request.POST.get('new-message')
    )
    room.participants.add(request.user)
    return redirect('room',pk=room.id)
  context={'room':room,'msgs':msgs,'participants':participants}
  return render(request,'base/room.html',context)

@login_required(login_url='/login')
def create(request):
  is_created = True
  form = RoomForm()
  topics = Topic.objects.all()
  # if request.method == "POST":
  #   form=RoomForm(request.POST)
  #   if form.is_valid():
  #     # form.save()
  #     room = form.save(commit=False)
  #     room.host = request.user
  #     room.save()
  #     return redirect('home')
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    Room.objects.create(
      host = request.user,
      topic = topic,
      name = request.POST.get('name'),
      description = request.POST.get('description')
    )
    return redirect('home')

  context = {'form':form,'is_created':is_created,'topics':topics}
  return render(request,'base/create-room.html',context)

def editRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  # if request.method == 'POST':
  #   form = RoomForm(request.POST,instance=room)
  #   if form.is_valid():
  #     form.save()
  #     return redirect('home')
  topics = Topic.objects.all()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room.topic = topic
    room.name = request.POST.get('name')
    room.description = request.POST.get('description')
    room.save()
    return redirect('home')
  context = {'form':form,'topics':topics,'room':room}
  return render(request,'base/create-room.html',context)

def deleteRoom(request,pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  context={'obj':room.name}
  return render(request,'base/delete-room.html',context)

def logoutPage(request):
  logout(request)
  return redirect('home')


def loginPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == 'POST':
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request,'用户不存在')
    
    user = authenticate(request,username = username,password = pwd)
    if user is not None:
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'用户名与密码不匹配')

  is_login_page = True
  context = {'is_login_page':is_login_page}
  return render(request,'base/login_register.html',context)

def registerPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  # form = UserCreationForm()
  form = MyRegisterUserForm()
  if request.method == 'POST':
    # form = UserCreationForm(request.POST)
    form = MyRegisterUserForm(request.POST)
    print(form)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'something wasn\'t right')
  context = {'form':form}
  return render(request,'base/login_register.html',context)

def user(request,pk):
  user = User.objects.get(id=pk)
  topics = Topic.objects.all()
  user_msgs = user.message_set.all().order_by('-created')
  user_rooms = user.room_set.all().order_by('-updated')
  context = {'user':user,'user_rooms':user_rooms,'topics':topics,'msgs':user_msgs}
  return render(request,'base/profile.html',context)

# def editUser(request,pk):
#   user = User.objects.get(id=pk)
#   form = UserForm(instance=user)
#   if request.method == 'POST':
    
#     user.username = request.POST.get('username')
#     user.first_name = request.POST.get('first_name')
#     user.email = request.POST.get('email')
#     user.avatar.url = request.POST.get('avatar')
#     user.bio = request.POST.get('bio')
#     user.save()
#     return redirect('home')
#   context={'form':form}
#   return render(request,'base/edit-profile.html',context)

def deleteMessage(request,pk):
  msg = Message.objects.get(id=pk)
  if request.method == 'POST':
    msg.delete()
    return redirect('home')
  context = {'obj':msg.content}
  return render(request,'base/delete-room.html',context)

@login_required(login_url='/login')
def moreTopic(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  
  topics = Topic.objects.filter(
    Q(name__icontains = q)
  )
  context = {'topics':topics}

  return render(request,'base/topics.html',context)

def setting(request):
  # user = User.objects.get(id=request.user.id)
  user = request.user
  form = UserForm(instance=user)
  # if request.method == 'POST':
  #   user.username = request.POST.get('username')
  #   user.first_name = request.POST.get('first_name')
  #   user.email = request.POST.get('email')
  #   user.avatar.url = request.POST.get('avatar')
  #   user.bio = request.POST.get('bio')
  #   user.save()
  #   return redirect('home')
  if request.method == 'POST':
    form = UserForm(request.POST,request.FILES,instance=user)
    if form.is_valid():
      form.save()
      return redirect('user',pk=user.id)
  context={'form':form}
  # return render(request,'base/settings.html',context)
  return render(request,'base/edit-profile.html',context)