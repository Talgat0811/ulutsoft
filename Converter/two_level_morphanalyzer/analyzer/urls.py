from django.urls import path
from .views import *
from analyzer import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(5)(AudiosHome.as_view()), name='home'),
    path('text_to_speech/', text_to_speech, name='text_to_speech'),
    #path('login/', login, name='login'),
    path('speech_to_text/', speech_to_text, name='speech_to_text'),
    path('audio_to_text/', audio_to_text, name='audio_to_text'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
