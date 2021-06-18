# HydroponicServer
HydroponicServer

# Установка
Склонируйте проект

```C:\dir>git clone https://github.com/Machalkas/HydroponicServer.git```

Настройте виртуальную среду

```C:\dir>py -m venv env```

Активируйте среду

```C:\dir>env\Scripts\activate.bat```

Установите библиотеки

```(env) C:\dir>pip install -r req.txt```

Установите Redis (аналог для Windows https://www.memurai.com/)

**Перед первым запуском**

Выполни миграции

```(env) C:\dir> py manage.py migrate```

**Запуск**

```(env) C:\dir> py manage.py runserver```
