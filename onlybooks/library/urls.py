from django.urls import path
from .views import Index,user_login,custom_logout,register

urlpatterns=[
    path('',Index,name='home_path'),
    path('useraccount/login/',user_login, name="login"),    
    path('logout/', custom_logout, name="logout"),
    path('useraccount/register/', register, name='register')
]