import random

import markdown, sys, os
import markdown
import time
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.core.cache import cache
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from analyzer.forms import *
from two_level_morphanalyzer import settings
from two_level_morphanalyzer.settings import MEDIA_URL
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.db import connection
from django.http import JsonResponse
import requests
from analyzer.speech2text import WhisperModel
#from analyzer.text2speech import TTS
import shutil

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import mimetypes
from django.http.response import HttpResponse, HttpResponseNotFound, Http404
from django.views.decorators.cache import cache_page
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Max
from pydub import AudioSegment
import secrets
import string

navbar = [
          # {'title': 'Кирүү', 'url': 'login'},
        {'title': 'Тексттен үнгө', 'url': 'text_to_speech'},{'title': 'Үндөн текстке', 'url': 'speech_to_text'},
        {'title': 'Аудиофайлдан текстке', 'url': 'audio_to_text'}
          ]

wav_mp3 = ['audio/x-wav','audio/wav', 'audio/mpeg']
context = {}
captcha_error = ['<ul class="errorlist"><li>captcha<ul class="errorlist"><li>Это поле обязательно для заполнения.</li></ul></li></ul>',
		'<ul class="errorlist"><li>captcha<ul class="errorlist"><li>Обязательное поле.</li></ul></li></ul>',
		'<ul class="errorlist"><li>captcha2<ul class="errorlist"><li>Это поле обязательно для заполнения.</li></ul></li></ul>',
		'<ul class="errorlist"><li>captcha2<ul class="errorlist"><li>Обязательное поле.</li></ul></li></ul>']
		
text_error = '<ul class="errorlist"><li>text<ul class="errorlist"><li>Кайра жазыңыз</li></ul></li></ul>'
file_result = ''
whisper_model = WhisperModel()
class AudiosHome(ListView):
    model = Audios
    template_name = 'analyzer/index.html'
    context_object_name = 'audios'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Башкы бет'
        context['navbar'] = navbar
        context['cat_selected'] = 0
        return context




#@cache_page(60 * 15)
@csrf_protect
@csrf_exempt
def text_to_speech(request):

    context = {}
    if request.method == 'POST':
        text = request.POST['text']
        choose = request.POST['choose']
        form = TextForm(request.POST)
        if form.is_valid():
            request.session['text'] = text
            api_url = 'http://127.0.0.1:6000/api/receive_data'  # Replace with your Flask API's URL
            if choose == 'man':
            	#obj = TTS('Нурбек', 48)
            	data_to_send = {"gender": "man", "text": text}  # Replace with your data
            	
            	response = requests.post(api_url, json=data_to_send)
            	if response.status_code == 200:
            		received_data = response.json()
            		#print(received_data)
            		# Process the received data as needed
            		old_path = '/mnt/ks/Works/bot_text2speech/'+str(received_data['audio_url'])+'.mp3'
            		file_name = str(received_data['audio_url'])[7:]
            		new_path = '/mnt/ks/Works/site/Converter/two_level_morphanalyzer/media/audios/'+str(file_name)+'.mp3'
            		shutil.move(old_path, new_path)
            		request.session['audio_url'] = file_name + '.mp3' 
            		Audios.objects.create(text=request.session['text'], audio_file=request.session['audio_url'])
            		request.session['audio_url'] = MEDIA_URL + request.session['audio_url']
            		response_data = {'audio_url': request.session['audio_url'], 'audio_text': request.session['text'], 'is_not_valid':
            		False, 'captcha_error': False, 'other_error': False, 'man': True}
            		return JsonResponse(response_data)
            	else:
            		# Handle API error gracefully
            		return JsonResponse({"error": "Failed to send/receive data"}, status=500)
            	
            else:
            	
            	data_to_send = {"gender": "woman", "text": text}
            	
            	response = requests.post(api_url, json=data_to_send)
            	if response.status_code == 200:
            		received_data = response.json()
            		#print(received_data)
            		# Process the received data as needed
            		old_path = '/mnt/ks/Works/bot_text2speech/'+str(received_data['audio_url'])+'.mp3'
            		file_name = str(received_data['audio_url'])[6:]
            		new_path = '/mnt/ks/Works/site/Converter/two_level_morphanalyzer/media/audios/'+str(file_name)+'.mp3'
            		shutil.move(old_path, new_path)
            		request.session['audio_url'] = file_name + '.mp3'
            		Audios.objects.create(text=request.session['text'], audio_file=request.session['audio_url'])
            		request.session['audio_url'] = MEDIA_URL + request.session['audio_url']
            		response_data = {'audio_url': request.session['audio_url'], 'audio_text': request.session['text'], 'is_not_valid':
            		False, 'captcha_error': False, 'other_error': False, 'man': False}
            		return JsonResponse(response_data)
            	else:
            		# Handle API error gracefully
            		return JsonResponse({"error": "Failed to send/receive data"}, status=500)
        else:
            #print(form.errors)	
            if str(form.errors) in captcha_error:
            	#print('captcha error')
            	response_data = {'captcha_error': True, 'is_not_valid': False, 'other_error': False}
            	return JsonResponse(response_data)
            elif str(form.errors) == text_error:
            	response_data = {'is_not_valid': True, 'other_error': False}
            	return JsonResponse(response_data)
            else:
            	response_data = {'other_error': True}
            	return JsonResponse(response_data)
            
    else:
        form = TextForm(request.POST)
    context = {
        'title': 'Тексттен үнгө',
        'navbar': navbar,
        'form': form,
    }
    return render(request, "analyzer/audio.html", context=context)



#@cache_page(60 * 15)
@csrf_protect
@csrf_exempt
def audio_to_text(request):
    context = {}
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        audio_file = request.FILES['audio_file']
        file_type = request.FILES['audio_file'].content_type
        file_size = request.FILES['audio_file'].size
        print(file_type)
        if form.is_valid() and file_type in wav_mp3:
            if round((file_size/1024/1024),2) <= 5:
                #obj = form.save()
                request.session['audio_url'] = str(audio_file)
                sound = AudioSegment.from_file(audio_file)
                sound = sound.set_frame_rate(16000)
                sound.export(settings.MEDIA_ROOT+str(request.session['audio_url']), format="wav")
                request.session['text'] = whisper_model.generate_text_from_audio(settings.MEDIA_ROOT+request.session['audio_url'])
                Audios.objects.create(audio_file=request.session['audio_url'],text=request.session['text'])
                
                request.session['audio_url'] = MEDIA_URL + request.session['audio_url']
                response_data = {'audio_url': request.session['audio_url'], 'audio_text': request.session['text'],
                                 'is_not_valid2': False, 'is_not_valid': False}
                return JsonResponse(response_data)
            else:
                response_data = {'is_not_valid2': True, 'is_not_valid': False}
                return JsonResponse(response_data)
        else:
            if str(form.errors) in captcha_error:
                response_data = {'captcha_error': True, 'is_not_valid': False, 'is_not_valid2': False}
                return JsonResponse(response_data)
            else:
                response_data = {'is_not_valid': True, 'is_not_valid2': False}
                return JsonResponse(response_data)
    else:
        form = DocumentForm()
    context = {
        'title': 'Аудиофайлдан текстке',
        'navbar': navbar,
        'form': form
    }
    return render(request, "analyzer/audio3.html", context=context)


# class RegisterUser(CreateView):
#     form_class = UserCreationForm
#     template_name = 'analyzer/register.html'
#     success_url = reverse_lazy('login')
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#@cache_page(60 * 15)
@csrf_protect
@csrf_exempt
def speech_to_text(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        upload_dir = 'recorded/'
        N = 4
        
        res1 = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                      for i in range(N))
        res2 = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                       for i in range(N))
        audio_file_name = str(audio_file)[:-4]+'_'+str(res1)+'_'+str(res2)+'.wav'
        file_path = os.path.join(settings.MEDIA_ROOT, upload_dir, audio_file_name)
        
        #with open(file_path, 'wb') as destination:
        #    for chunk in audio_file.chunks():
        #        destination.write(chunk)

        request.session['audio_url_record'] = upload_dir + audio_file_name
        
        sound = AudioSegment.from_file(audio_file)
        sound = sound.set_frame_rate(16000)
        sound.export(settings.MEDIA_ROOT+str(request.session['audio_url_record'][:-4])+'_new.wav', format="wav")
        request.session['audio_url_record'] = str(request.session['audio_url_record'][:-4])+'_new.wav'
        
        #st = time.time()
        request.session['text_record'] = whisper_model.generate_text_from_audio(settings.MEDIA_ROOT+request.session['audio_url_record'])
        #et = time.time()
        #elapsed_time = et - st
        #print('Execution time:', elapsed_time, 'seconds')
        print(request.session['text_record'])
        Audios.objects.create(audio_file=request.session['audio_url_record'],text=request.session['text_record'])
        request.session['audio_url_record'] = MEDIA_URL + request.session['audio_url_record']
        request.session['audio_save'] = True
        context = {
            'title': 'Үндөн текстке',
            'navbar': navbar,
            'is_not_valid': False,
            'record': request.session['audio_url_record'],
            'record_text': request.session['text_record']
        }
        return JsonResponse({'success': True, 'audio_url': request.session['audio_url_record'], 'text': request.session['text_record']})
    else:
        if 'audio_save' in request.session and request.session['audio_save']:
            context = {
                'title': 'Үндөн текстке',
                'navbar': navbar,
                'record': request.session['audio_url_record'],
                'record_text': request.session['text_record']
            }
            request.session['audio_save'] = False
            return render(request, "analyzer/audio2.html", context=context)

        context = {
            'title': 'Үндөн текстке',
            'navbar': navbar,
            'record': False,
            'record_text': False
        }
        return render(request, "analyzer/audio2.html", context=context)
@cache_page(60 * 15)
@csrf_protect
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = User_nameForm(request.POST)
        form2 = TextForm(request.POST)
        if form.is_valid():
            user_name = request.POST["user_name"]
            qset = Users.objects.values('pk').filter(user_name=user_name).first()
            if qset:
                if 'name' in request.session and request.session['name']==user_name:
                    qset = Users.objects.values('pk').filter(user_name=request.session['name']).first()
                    # print(qset)
                    request.session['user_id'] = qset['pk']
                    request.session['s_num'] = Users.objects.values('number').filter(
                        id=request.session['user_id']).first()
                    #print('name is exist')
                    qset = Audios.objects.values('pk').filter(status=False, is_correct=False)
                    request.session['s_id_list'] = list(qset)
                    #print(request.session['s_id_list'])
                    if not request.session['s_id_list']:
                        context = {
                            'no_audio': True,
                            'title': 'Башкы бет',
                            'navbar': navbar,
                            'user_name': request.session['name']
                        }
                        return render(request, "analyzer/index.html", context=context)
                    request.session['audios_id'] = random.choice(list([i['pk'] for i in request.session['s_id_list']]))
                    qset = Audios.objects.values('audio_file').filter(id=request.session['audios_id']).first()
                    request.session['audio_url'] = qset['audio_file']
                    request.session['audio_url'] = MEDIA_URL + request.session['audio_url']
                    context = {
                        'title': 'Угуп жазуу',
                        'navbar': navbar,
                        'form': form2,
                        'audio_id': request.session['audios_id'],
                        'audio_file_url': request.session['audio_url'],
                        'is_not_valid': False,
                        'finished_sound_number': request.session['s_num']['number']
                    }
                    return render(request, "analyzer/audio.html", context=context)
                    #return redirect("audio", audio_id=request.session['audios_id'])

                else:
                    request.session['name'] = user_name
                    qset = Users.objects.values('pk').filter(user_name=request.session['name']).first()
                    # print(qset)
                    request.session['user_id'] = qset['pk']
                    request.session['s_num'] = Users.objects.values('number').filter(
                        id=request.session['user_id']).first()
                    #print('name is not exist')
                    qset = Audios.objects.values('pk').filter(status=False, is_correct=False)
                    request.session['s_id_list'] = list(qset)
                    #print(request.session['s_id_list'])
                    if not request.session['s_id_list']:
                        context = {
                            'no_audio': True,
                            'title': 'Башкы бет',
                            'navbar': navbar,
                            'user_name': request.session['name']
                        }
                        return render(request, "analyzer/index.html", context=context)
                    request.session['audios_id'] = random.choice(list([i['pk'] for i in request.session['s_id_list']]))
                    qset = Audios.objects.values('audio_file').filter(id=request.session['audios_id']).first()
                    request.session['audio_url'] = qset['audio_file']
                    request.session['audio_url'] = MEDIA_URL + request.session['audio_url']
                    context = {
                        'title': 'Угуп жазуу',
                        'navbar': navbar,
                        'form': form2,
                        'audio_id': request.session['audios_id'],
                        'audio_file_url': request.session['audio_url'],
                        'is_not_valid': False,
                        'finished_sound_number': request.session['s_num']['number']
                    }
                    return render(request, "analyzer/audio.html", context=context)
                    #return redirect("audio", audio_id=request.session['audios_id'])
            else:
                form = User_nameForm()
                user_not_found = True
                context = {
                    'title': 'title',
                    'navbar': navbar,
                    'form': form,
                    'user_name': user_name,
                    'user_not_found': user_not_found
                }
                return render(request, 'analyzer/login.html', context=context)
    else:
        form = User_nameForm(request.POST)
    context = {
        'title': 'Login',
        'navbar': navbar,
        'form': form,
    }
    return render(request, 'analyzer/login.html', context=context)




