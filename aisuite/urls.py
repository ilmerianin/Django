#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 01:11:54 2022

@author: wasilii
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
#from django.conf.urls import url
from django.urls import include, re_path
       #функция url() определяет регулярное выражение (r'^books/$'), связывающее URL-адрес с функцией отображения

urlpatterns = [
    re_path(r'predict_image$', views.predAI), # /predict_image
    path('', views.indexai, name='indexai'),
            # функцию отображения, которая будет вызвана, если введённый адрес будет соответствует данному паттерну (views.index — это функция с именем index() в views.py).

  
]    
  #(views.BookListView.as_view() ), которая будет вызвана, если URL-адрес будет соответствовать паттерну РВ.
        #Данное РВ сопоставляет любой URL-адрес, который начинается с book/, за которым до конца строки (до маркера конца строки - $) следуют одна, или более цифр. В процессе выполнения данного преобразования, оно "захватывает" цифры и передаёт их в функцию отображения как параметр с именем pk.
        # https://docs.python.org/3/library/re.html  Паттерны регулярного выражения является невероятно мощным
        
    