from django.contrib import admin

from wodmovements.models import Movement
from wods.models import Workout

admin.site.register(Movement)
admin.site.register(Workout)
