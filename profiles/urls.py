from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', TemplateView.as_view(template_name='profiles/profile.html'), name='profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
