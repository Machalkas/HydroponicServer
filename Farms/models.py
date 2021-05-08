from django.db import models
from Users.models import User

class Farm(models.Model):
    name=models.CharField(max_length=100, blank=True, null=False, default="Ферма", verbose_name="Название")
    token=models.CharField(max_length=200, blank=False, null=False, unique=True, verbose_name="Токен")
    create_date=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_public=models.BooleanField(blank=True, null=False, default=False, verbose_name="Публичный доступ")
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    class Meta:
        verbose_name = 'Ферма'
        verbose_name_plural = 'Фермы'
    def __str__(self):
        return self.name
    
class Statistic(models.Model):
    record_date=models.DateTimeField(blank=False, null=False, verbose_name="Дата записи")
    ph=models.FloatField(blank=True, null=True, verbose_name="PH")
    tds=models.FloatField(blank=True, null=True, verbose_name="TDS")
    air_temp=models.FloatField(blank=True, null=True, verbose_name="Температура воздуха")
    humidity=models.FloatField(blank=True, null=True, verbose_name="Влажность воздуха")
    water_temp=models.FloatField(blank=True, null=True, verbose_name="Температура раствора")
    co2=models.FloatField(blank=True, null=True, verbose_name="CO2")
    max_level=models.BooleanField(blank=True, null=True, verbose_name="Максимальный уровень раствора")
    min_level=models.BooleanField(blank=True, null=True, verbose_name="Минимальный уровень раствора")
    sensors_tank_level=models.BooleanField(blank=True, null=True, verbose_name="Минимальный уровень бака для датчиков")
    farm=models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Ферма")
    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
    def __str__(self):
        return self.record_date+'|'+self.farm

class Timetable(models.Model):
    date=models.DateField(blank=False, null=False, verbose_name="Дата")
    light_on_time=models.TimeField(blank=True, null=True, verbose_name="Включение света")
    light_off_time=models.TimeField(blank=True, null=True, verbose_name="Выключение света")
    solution1=models.PositiveIntegerField(blank=True, null=False, default=0, verbose_name="Раствор1")
    solution2=models.PositiveIntegerField(blank=True, null=False, default=0, verbose_name="Раствор2")
    solution3=models.PositiveIntegerField(blank=True, null=False, default=0, verbose_name="Раствор3")
    co2=models.PositiveIntegerField(blank=True, null=False, default=0, verbose_name="CO2")
    farm=models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Ферма")
    class Meta:
        verbose_name='Расписание'
        verbose_name_plural='Расписание'
    def __str__(self):
        return self.date+'|'+self.farm

class Parameters(models.Model):
    parameters=models.JSONField(blank=False, null=False, verbose_name="Параметры")
    record_date=models.DateTimeField(blank=False, null=False, verbose_name="Дата записи")
    farm=models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Ферма")
    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметры'
    def __str__(self):
        return self.record_date+'|'+self.farm




