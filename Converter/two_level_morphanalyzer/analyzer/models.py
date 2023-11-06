from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from ckeditor.fields import RichTextField




class Audios(models.Model):
    audio_file = models.FileField(upload_to='', verbose_name="Аудио файл")
    text = models.TextField(blank=True)
    # super_visor = models.CharField(max_length=20)
    # admin = models.CharField(max_length=20)
    # status = models.BooleanField(default=False)
    # is_correct = models.BooleanField(default=False)
    #user_name = models.ForeignKey('Users', on_delete=models.PROTECT, null=True)
    @property
    def sound_display(self):
        if self.audio_file:
            #{self.audio_file.url}
            return mark_safe(f'<audio controls style="width: 300px;" name="media"><source src="{self.audio_file.url}" type="audio/wav"></audio>')
        return ""
    def __str__(self):
        return f" {self.audio_file.url}"

    def get_absolute_url(self):
        return reverse('audio', kwargs={'audio_id': self.pk})

    def save(self, *args, **kwargs):
        super(Audios, self).save(*args, **kwargs)
        return self
    class Meta:
        ordering = ['audio_file']

class Users(models.Model):
    user_name = models.CharField(max_length=20, blank=True, db_index=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return f" {self.user_name}"