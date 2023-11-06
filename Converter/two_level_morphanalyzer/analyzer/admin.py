from django.contrib import admin
from django.forms import TextInput
from django.utils.safestring import mark_safe

from . import models

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django import forms
from .models import Audios, Users
from django.utils.html import format_html



class AudiosAdmin(admin.ModelAdmin):
    #form = MyModel
    list_display = ('id', 'get_audio', 'get_text', 'sound_display')
    list_display_links = ('id', 'get_audio')
    search_fields = ('text', 'audio_file')
    #list_filter = ('status','is_correct','super_visor', 'user_name' ,'admin')
    #list_editable = ('text', )
    fields = ('audio_file', 'text')
    #prepopulated_fields = {"slug": ("audio_file",)}

    def get_audio(self, object):
        if object.audio_file:
            wav_name = str(object.audio_file)
            if len(wav_name)>27:
                wav_name = wav_name[:27] + '...'
            return mark_safe(f"<div style='max-width: 20px table-layout:fixed' >{wav_name}</div>")
    def get_text(self, object):
        if object.text:
            return mark_safe(f"<p style='width: 430px; word-wrap: break-word; font-size: 16px'>{object.text}</p>")
    def check_box(self, object):
        if object.text:
            return mark_safe(f"<p style='width: 180px; word-wrap: break-word;'>{object.text}</p>")
    def sound_display(self, item):
        return item.sound_display

    sound_display.short_description = 'sound'
    sound_display.allow_tags = True
    get_text.short_description = 'Text'
    get_audio.short_description = 'Audio'

class UsersAdmin(admin.ModelAdmin):
    #form = MyModel
    list_display = ('id', 'user_name', 'number')
    list_display_links = ('id', )
    search_fields = ('user_name',)
    list_filter = ('user_name',)
    list_editable = ( 'number',)
    fields = ('user_name','number')
admin.site.register(Audios, AudiosAdmin)
admin.site.register(Users, UsersAdmin)
