from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
