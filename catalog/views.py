from django.shortcuts import render
            #https://docs.djangoproject.com/en/1.10/topics/http/shortcuts/#django.shortcuts.render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=len([bok for bok in BookInstance.objects.all() if 'труд'  in bok.book.title.lower() ])  #BookInstance.objects.all().count()
    # Доступные книги (статус = 'a') https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Models#searching_for_records
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genre = len([genr for genr in Genre.objects.all() if 'нт'  in genr.name.lower() ])  # Метод 'all()' применён по умолчанию

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(  #оторая, в качестве ответа, создаёт и возвращает страницу HTML 
        request,       #объект request (типа HttpRequest)
        'index.html',  # catalog/templates/index.html  шаблон HTML-страницы с метками (placeholders), которые будут замещены данными,
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genre':num_genre},
    )  # Django ищет файлы шаблонов в директории с именем 'templates' внутри вашего приложения.

from django.views import generic

class BookListView(generic.ListView): # создает клас для передаыи всех через url
    model = Book #Это всё! Обобщённое отображение выполнит запрос к базе данных, получит все записи заданной модели (Book), затем отрендерит (отрисует) соответствующий шаблон, расположенный в /locallibrary/catalog/templates/catalog/book_list.html 
                # Внутри данного шаблона вы можете получить доступ к списку книг при помощи переменной шаблона object_list ИЛИ book_list (если обобщить, то "the_model_name_list").
class AuthorListView(generic.ListView): # создает клас для передаыи всех через url
    model = Author # object_list ИЛИ author_list формируются тут
 
class BookDetalView(generic.detail.DetailView):
    model = Book

class AuthorDetalView(generic.detail.DetailView):
    model = Author



