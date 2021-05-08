from django.contrib import admin
from .models import Farm, Statistic, Timetable, Parameters

admin.site.register(Farm)
admin.site.register(Statistic)
admin.site.register(Timetable)
admin.site.register(Parameters)