from django.contrib import admin

from .models import Workout, Athlete

admin.site.register(Athlete)
admin.site.register(Workout)
