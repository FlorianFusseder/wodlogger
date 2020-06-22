from django.contrib import admin

from wodmovements.models import Movement
from wods.models import Workout, Component

admin.site.register(Movement)
admin.site.register(Component)
admin.site.register(Workout)
