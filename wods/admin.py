from django.contrib import admin

from wodmovements.models import Movement, Component
from wods.models import Workout

admin.site.register(Movement)
admin.site.register(Component)
admin.site.register(Workout)
