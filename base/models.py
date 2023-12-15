from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User (AbstractUser):
  # username = models.CharField(max_length=20,null=True,unique=True)
  name = models.CharField(max_length=20,null=True)
  email = models.EmailField(unique=True,null=True)
  bio = models.TextField(null=True)
  avatar = models.ImageField(null=True,default='avatar.svg')

  # USERNAME_FIELDS = 'username'
  USERNAME_FIELDS = ['username', 'email']
  REQUIRED_FIELDS = []

class Topic(models.Model):
  name = models.CharField(max_length=20)

  def __str__(self):
    return self.name
  
class Room(models.Model):
  host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
  participants = models.ManyToManyField(User,related_name='Participant',blank=True)
  name = models.CharField(max_length=100)
  description = models.TextField(null=True,blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  
class Message(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  room = models.ForeignKey(Room,on_delete=models.CASCADE,null=True)
  content = models.TextField(max_length=200)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.content[0:50]