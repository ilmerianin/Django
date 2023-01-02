#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 01:11:54 2022

@author: wasilii
"""

#from django.urls import path
from . import views
#from django.conf.urls import url
from django.urls import include, re_path
       #функция url() определяет регулярное выражение (r'^books/$'), связывающее URL-адрес с функцией отображения

urlpatterns = [
    #path('', views.index, name='index'),
            # функцию отображения, которая будет вызвана, если введённый адрес будет соответствует данному паттерну (views.index — это функция с именем index() в views.py).
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'), #получаем доступ к соответствующей функции отображения при помощи вызова метода as_view(). Таким образом выполняется вся работа по созданию экземпляра класса и гарантируется вызов правильных методов для входящих HTTP-запросов.
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'), # aформирование адреса и  набора авторов
    #  ключ фраза после отбора,  список autor_list.фя отображ(ищет фай/catalog/autor_list.) name=приставка к внутр адресу 
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetalView.as_view(), name='book-detail'), # формируется динамически с отданного от get_absolute_url  
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetalView.as_view(), name='author-detail'), # формируется динамически с отданного от get_absolute_url  
]      #(views.BookListView.as_view() ), которая будет вызвана, если URL-адрес будет соответствовать паттерну РВ.
        #Данное РВ сопоставляет любой URL-адрес, который начинается с book/, за которым до конца строки (до маркера конца строки - $) следуют одна, или более цифр. В процессе выполнения данного преобразования, оно "захватывает" цифры и передаёт их в функцию отображения как параметр с именем pk.
        # https://docs.python.org/3/library/re.html  Паттерны регулярного выражения является невероятно мощным
        
       