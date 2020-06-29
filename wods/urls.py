from django.urls import path

from . import views
from .views import create_workout

app_name = 'wods'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/update', views.UpdateView.as_view(), name='update', ),
    path('<int:pk>/delete', views.DeleteView.as_view(), name='delete'),
    path('create/', create_workout, name='create'),
    path('<int:pk>/add_score', views.AddScoreView.as_view(), name='add_score')
]
