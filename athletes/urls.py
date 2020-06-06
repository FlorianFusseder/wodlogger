from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'athletes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', TemplateView.as_view(template_name='athletes/athlete_profile.html'), name='profile'),
]