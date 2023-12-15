from django.urls import path
from . import views

urlpatterns = [
    path('logout',views.logoutPage,name='logout'),
    path('login',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),

    path('',views.home,name='home' ),
    path('room/<str:pk>',views.room,name='room'),
    path('user/<str:pk>',views.user,name='user'),

    path('create',views.create,name='create'),
    path('edit/<str:pk>',views.editRoom,name='edit'),
    path('delete/<str:pk>',views.deleteRoom,name='delete'),
    path('delete-msg/<str:pk>',views.deleteMessage,name='delete-msg'),
    
    path('more-topic',views.moreTopic,name='more-topic'),
    path('setting',views.setting,name='setting'),
    # path('edit-user/<str:pk>',views.editUser,name='edit-user')
]
