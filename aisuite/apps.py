from django.apps import AppConfig


class AisuiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aisuite"    #  Этот атрибут определяет, к какому приложению применяется конфигурация. Он должен быть определен во всех подклассах AppConfig .
    #label =   #Краткое название приложения, например
    verbose_name  = 'Демо нейросеть' # Понятное имя приложения, например. «Администрация». По умолчанию этот атрибут эквивалентен label.title() .
    #path #Путь файловой системы к каталогу приложения, например. '/usr/lib/pythonX.Y/dist-packages/django/contrib/admin' ,
    
    
    