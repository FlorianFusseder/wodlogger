from django.urls import path

from . import views

app_name = 'wods'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:workout_id>/', views.detail, name='detail'),
    path('create/<int:workout_id/>', views.create, name='create'),
]
