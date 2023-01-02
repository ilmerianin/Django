from django.shortcuts import render
from app_keras_suite import predictImage
from django.http import HttpResponse
# Create your views here.
def indexai(request):   
    """
    Функция отображения для домашней страницы сайта.
    """
    
    return render(  #оторая, в качестве ответа, создаёт и возвращает страницу HTML 
        request,       #объект request (типа HttpRequest)
        'indexai.html',  # catalog/templates/index.html  шаблон HTML-страницы с метками (placeholders), которые будут замещены данными,
        #context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genre':num_genre},
    )  # Django ищет файлы шаблонов в директории с именем 'templates' внутри вашего приложения.

def predAI(request):
    answer = predictImage(request)
    print('Пришел/ Пошел  POST')
    return HttpResponse(answer)