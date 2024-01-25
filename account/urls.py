
from django.urls import path
from .views import  RegisterView,logout_view,user_login


urlpatterns = [
   
    path('login/',user_login,name='login'),
    path('logout/',logout_view,name='logout'),
    path('register/', RegisterView.as_view(),name='register'),

]