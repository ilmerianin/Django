#from flask import Flask, jsonify, request
from PIL import Image
import time
import numpy as np # Импортируем библиотеку numpy
import requests
import json
import sys

from tensorflow.keras.models import Model # Импортируем модели keras: Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, concatenate, Activation, MaxPooling2D, Conv2D, BatchNormalization, Flatten, Dense, Dropout, Conv2DTranspose, Concatenate, Reshape
#from tensorflow.keras.optimizers import Adam # Импортируем оптимизатор Adam
from tensorflow.keras.models import model_from_json


# Загружаем нашу обученную нейросеть
json_file = open("model/digitals-model.json", "r")
model_json = json_file.read()
json_file.close()
# Восстанавливаем нашу модель из данных, которые хранятся в файле
model = model_from_json(model_json)
# Загружаем веса модели
model.load_weights('model/digitals-weights.hdf5')
model.summary()

# Создаем наше веб-приложение
#app = Flask(__name__)

# Функция проверки формата изображения - альбомный или книжный.
# Возвращаемые значения: True - альбомный, False - книжный
def format_is_album(w: int, h: int):
    return True if w > h else False


# Функция умной обрезки
def smart_trimming(img):
    img_w, img_h = img.size   # Берём размер картинки
    target_size = [28, 28]  # Размер, который мы должны получить в результате

    # Проверка на формат
    if format_is_album(img_w, img_h):
        new_h = target_size[1]                # Делаем высоту основной осью
        new_w = round(new_h / img_h * img_w)  # Считаем ширину
    else:
        new_w = target_size[0]                # Делаем ширину основной осью
        new_h = round(new_w / img_w * img_h)  # Считаем высоту

    # Применяем наши измениния касательно размеров
    img = img.resize((new_w, new_h), Image.ANTIALIAS)

    # Находим центр картинки
    center = [new_w//2, new_h//2]
    # Находим левую верхнюю и правую нижнюю точки для прямоугольной обрезки
    top_left = [center[0] - target_size[0]//2, center[1] - target_size[1]//2]
    bottom_right = [center[0] + target_size[0]//2, center[1] + target_size[1]//2]

    # Обрезаем изображение
    img = img.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))

    return img



# =============================================================================
# 
# @app.route('/')
# def index():
#     index = open("static/index.html", "r")
#     page = index.read()
#     index.close()
#     return page
# 
# =============================================================================

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import QueryDict
import os
from django.http import JsonResponse

from io import BytesIO
from PIL import Image


#@app.route('/predict_image', methods=['POST'])
def predictImage(request):
# =============================================================================
#     print('predictImage: ', type(request), request)
#     print(type(request)) # <class 'django.core.handlers.wsgi.WSGIRequest'>
#     print(request.GET)   # <QueryDict: {}>
#     print("request.POST: ",request.POST)  #<QueryDict: {'key': ['---44---']}>
#     print("request.FILES ", request.FILES)
#     print('request.COOKIES)',request.COOKIES)
#     print('request.session:',request.session)
#     print('request.META:',request.META)
#     print(request.META["HTTP_HOST"])     # 127.0.0.1:8000
#     print(request.META["HTTP_REFERER"])  # http://127.0.0.1:8000/aisuite/
#     #data = QueryDict('status=error', mutable=True)
# =============================================================================
    data = {'status': 'ok'}
    image = request.FILES['image']
    key = request.POST['key']

    if image:
        print()
        print("Начинаем оработку картинки")
        imageFile = 'static/image/upload_image.jpg'
        path = default_storage.save( imageFile , ContentFile(image.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        #image.save(imageFile) 

        # Уменьшаем и обрезаем изображение (пока оно у нас в виде объекта Pillow)
        image_crop = Image.open(tmp_file).convert('L')
        print(tmp_file)
        image_crop = smart_trimming(image_crop)
        corimageFile = 'static/image/cropped_image.jpg'
        
        file_buffer = BytesIO()     # сщздать  поток
        image_crop.save(file_buffer, 'png') # запулить в поток
        
        #print(dir(image_crop), type(image_crop))
        path1 = default_storage.save( corimageFile , ContentFile(file_buffer.read())) #через поток
        tmp_file2 = os.path.join(settings.MEDIA_ROOT, path1)
        #image_crop.save(os.path.join(settings.MEDIA_ROOT, 'static/images/cropped_image.jpg')
        file_buffer.close() # закрыть
        # Преобразуем объект Pillow в массив
        image_array = np.array(image_crop)

        # Получаем одномерный массив
        data_for_predict = image_array.reshape(1, 28*28)
        # Инвертируем изображение
        data_for_predict = 255-data_for_predict
        # Нормализуем изображение
        data_for_predict = data_for_predict / 255
        
        #print(data_for_predict)

        # Подаем данные в нашу модель и получаем ответы
        prediction = model.predict(data_for_predict)
       
        

        # Берем нулевой элемент, т.к. подали только одну картинку
        result = prediction[0]

        predict_digit = np.argmax(result)

        print("Ответ нейронки: ", result)
        print("Ответ: ", predict_digit)

        data['status'] = 'ok'
        data['image_link'] = tmp_file
        data['image_source_link'] = tmp_file2
        data['answer'] = str(predict_digit)
    
        print(data)
        query_dict = QueryDict('', mutable=True)
        
        query_dict.update(data)
        print(query_dict)
        
    return JsonResponse(data)

#app.run(debug=True, host='ai.role.ru', port=1100)
'''
predictImage:  <class 'django.core.handlers.wsgi.WSGIRequest'> <WSGIRequest: POST '/aisuite/predict_image'>
<class 'django.core.handlers.wsgi.WSGIRequest'>
<QueryDict: {}>
request.POST:  <QueryDict: {'key': ['---44---']}>
request.FILES  <MultiValueDict: {'image': [<InMemoryUploadedFile: cropped_image.jpg (image/jpeg)>]}>
request.COOKIES) {'csrftoken': 'uOAcICTjjpwd0lqMLs0erDYuPhfLRcIa', 'sessionid': '46kz6ee112r69qkm2n46ut6yip17r63o'}
request.session: <django.contrib.sessions.backends.db.SessionStore object at 0x7fdef53002b0>
request.META: {'SHELL': '/bin/bash', 'SESSION_MANAGER': 'local/as-es:@/tmp/.ICE-unix/982,unix/as-es:/tmp/.ICE-unix/982', 'QT_ACCESSIBILITY': '1', 'QT_SCREEN_SCALE_FACTORS': '', 'COLORTERM': 'truecolor', 'SPYDER_ARGS': '[]', 'XDG_CONFIG_DIRS': '/etc/xdg/xdg-ubuntu:/etc/xdg', 'SSH_AGENT_LAUNCHER': 'gnome-keyring', 'XDG_MENU_PREFIX': 'gnome-', 'GNOME_DESKTOP_SESSION_ID': 'this-is-deprecated', 'SPY_FORMAT_O': '0', 'CONDA_EXE': '/home/wasilii/anaconda3/bin/conda', 'SPY_TESTING': 'False', '_CE_M': '', 'LANGUAGE': 'ru', 'LC_ADDRESS': 'es_MX.UTF-8', 'GNOME_SHELL_SESSION_MODE': 'ubuntu', 'SPY_USE_FILE_O': 'False', 'LC_NAME': 'es_MX.UTF-8', 'SSH_AUTH_SOCK': '/run/user/1000/keyring/ssh', 'SPY_WIDTH_O': '6', 'SPY_UMR_ENABLED': 'True', 'SPY_AUTOLOAD_PYLAB_O': 'False', 'SPY_PYLAB_O': 'True', 'XMODIFIERS': '@im=ibus', 'DESKTOP_SESSION': 'ubuntu', 'LC_MONETARY': 'es_MX.UTF-8', 'SPY_SYMPY_O': 'False', 'GTK_MODULES': 'gail:atk-bridge', 'PWD': '/home/wasilii/anaconda3/envs/DjangoSite/myprojectdir/myproject', 'LOGNAME': 'wasilii', 'XDG_SESSION_DESKTOP': 'ubuntu', 'CONDA_ROOT': '/home/wasilii/anaconda3', 'XDG_SESSION_TYPE': 'wayland', 'CONDA_PREFIX': '/home/wasilii/anaconda3/envs/DjangoSite', 'SYSTEMD_EXEC_PID': '1176', 'SPY_UMR_NAMELIST': '', '_': '/home/wasilii/anaconda3/envs/DjangoSite/bin/python', 'XAUTHORITY': '/run/user/1000/.mutter-Xwaylandauth.TZNGY1', 'SPY_BACKEND_O': '0', 'HOME': '/home/wasilii', 'USERNAME': 'wasilii', 'IM_CONFIG_PHASE': '1', 'SPY_HEIGHT_O': '4', 'LANG': 'ru_RU.UTF-8', 'LC_PAPER': 'es_MX.UTF-8', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:', 'XDG_CURRENT_DESKTOP': 'ubuntu:GNOME', 'SPYDER_DEBUG_FILE': '/home/wasilii/.config/spyder-py3/spyder-debug.log', 'VTE_VERSION': '6800', 'WAYLAND_DISPLAY': 'wayland-0', 'CONDA_PROMPT_MODIFIER': '(DjangoSite) ', 'PYDEVD_USE_FRAME_EVAL': 'NO', 'GNOME_TERMINAL_SCREEN': '/org/gnome/Terminal/screen/d0c70075_7d8c_42dd_9d55_182bcb0ca1ba', 'CLICOLOR': '1', 'SPY_RUN_FILE_O': '', 'SPY_PYTHONPATH': '', 'SPY_EXTERNAL_INTERPRETER': 'False', 'GNOME_SETUP_DISPLAY': ':1', 'JPY_PARENT_PID': '25544', 'LESSCLOSE': '/usr/bin/lesspipe %s %s', 'XDG_SESSION_CLASS': 'user', 'TERM': 'xterm-color', 'LC_IDENTIFICATION': 'es_MX.UTF-8', 'SPY_BBOX_INCHES_O': 'True', '_CE_CONDA': '', 'LESSOPEN': '| /usr/bin/lesspipe %s', 'USER': 'wasilii', 'GIT_PAGER': 'cat', 'SPY_GREEDY_O': 'False', 'GNOME_TERMINAL_SERVICE': ':1.199', 'SPY_RUN_LINES_O': '', 'CONDA_SHLVL': '2', 'SPY_AUTOCALL_O': '0', 'DISPLAY': ':0', 'SPY_HIDE_CMD': 'True', 'SHLVL': '2', 'PAGER': 'cat', 'LC_TELEPHONE': 'es_MX.UTF-8', 'QT_IM_MODULE': 'ibus', 'LC_MEASUREMENT': 'es_MX.UTF-8', 'MPLBACKEND': 'module://matplotlib_inline.backend_inline', 'CONDA_PYTHON_EXE': '/home/wasilii/anaconda3/bin/python', 'XDG_RUNTIME_DIR': '/run/user/1000', 'CONDA_DEFAULT_ENV': 'DjangoSite', 'LC_TIME': 'es_MX.UTF-8', 'XDG_DATA_DIRS': '/usr/share/ubuntu:/home/wasilii/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop', 'SPY_UMR_VERBOSE': 'True', 'PATH': '/home/wasilii/anaconda3/envs/DjangoSite/bin:/home/wasilii/anaconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin', 'GDMSESSION': 'ubuntu', 'SPY_JEDI_O': 'False', 'DBUS_SESSION_BUS_ADDRESS': 'unix:path=/run/user/1000/bus', 'CONDA_PREFIX_1': '/home/wasilii/anaconda3', 'QT_SCALE_FACTOR': '', 'SPY_RESOLUTION_O': '60', 'LC_NUMERIC': 'es_MX.UTF-8', 'DJANGO_SETTINGS_MODULE': 'myproject.settings', 'TZ': 'Europe/Moscow', 'RUN_MAIN': 'true', 'SERVER_NAME': 'localhost', 'GATEWAY_INTERFACE': 'CGI/1.1', 'SERVER_PORT': '8000', 'REMOTE_HOST': '', 'CONTENT_LENGTH': '885', 'SCRIPT_NAME': '', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SERVER_SOFTWARE': 'WSGIServer/0.2', 'REQUEST_METHOD': 'POST', 'PATH_INFO': '/aisuite/predict_image', 'QUERY_STRING': '', 'REMOTE_ADDR': '127.0.0.1', 'CONTENT_TYPE': 'multipart/form-data; boundary=----WebKitFormBoundarybPLWm8lUgp1ccjPK', 'HTTP_HOST': '127.0.0.1:8000', 'HTTP_CONNECTION': 'keep-alive', 'HTTP_SEC_CH_UA': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"', 'HTTP_SEC_CH_UA_MOBILE': '?0', 'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'HTTP_ACCEPT': 'application/json, text/javascript, */*; q=0.01', 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 'HTTP_X_CSRFTOKEN': 'uOu4pvtrDaC7Rfb093w3MhWQyKiGUKCHOsU6XXcAMpYaHqrCKlm73KKadRnhBMaH', 'HTTP_SEC_CH_UA_PLATFORM': '"Linux"', 'HTTP_ORIGIN': 'http://127.0.0.1:8000', 'HTTP_SEC_FETCH_SITE': 'same-origin', 'HTTP_SEC_FETCH_MODE': 'cors', 'HTTP_SEC_FETCH_DEST': 'empty', 'HTTP_REFERER': 'http://127.0.0.1:8000/aisuite/', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 'HTTP_ACCEPT_LANGUAGE': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'HTTP_COOKIE': 'csrftoken=uOAcICTjjpwd0lqMLs0erDYuPhfLRcIa; sessionid=46kz6ee112r69qkm2n46ut6yip17r63o', 'wsgi.input': <django.core.handlers.wsgi.LimitedStream object at 0x7fdef52f2490>, 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, 'wsgi.version': (1, 0), 'wsgi.run_once': False, 'wsgi.url_scheme': 'http', 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.file_wrapper': <class 'wsgiref.util.FileWrapper'>, 'CSRF_COOKIE': 'uOAcICTjjpwd0lqMLs0erDYuPhfLRcIa'}
'''

#ordinary_dict = {'a': 'one', 'b': 'two', }

