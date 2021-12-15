from django.contrib import admin
from .models import Farm, Statistic, Timetable, Parameters

class StatisticAdmin(admin.ModelAdmin):
    model=Statistic
    list_display=('record_date','farm','ph','tds','air_temp','humidity','water_temp','co2')
    list_filter=('record_date',)
    search_fields=('farm','record_date')
    ordering=('record_date',)

class FarmAdmin(admin.ModelAdmin):
    model=Farm
    list_display=('user','name',)
    search_fields=('name','user')
    ordering=('user',)

class TimetableAdmin(admin.ModelAdmin):
    model=Timetable
    list_display=('farm','date','light_on_time','light_off_time','solution1','solution2','solution3','co2')
    search_fields=('farm','date')
    ordering=('farm',)

admin.site.register(Farm,FarmAdmin)
admin.site.register(Statistic,StatisticAdmin)
admin.site.register(Timetable,TimetableAdmin)
admin.site.register(Parameters)