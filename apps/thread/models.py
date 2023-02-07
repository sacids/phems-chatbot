from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Thread(models.Model):
    """Thread Model"""
    ACTION_URL_OPTIONS = (
        ('PUSH', 'PUSH'),
        ('CREATE', 'CREATE'),
    )

    title       =  models.TextField(blank=False, null=False)
    flag        =  models.CharField(max_length=50, blank=False, null=False)
    label       =  models.CharField(max_length=50, blank=True, null=True)
    pull        =  models.IntegerField(default=0, null=False)
    url         =  models.CharField(max_length=200, blank=True, null=True)
    action      =  models.CharField(max_length=20, choices=ACTION_URL_OPTIONS, blank=True, null=True)
    action_url  =  models.CharField(max_length=200, blank=True, null=True)
    created_by  =  models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    updated_by  =  models.ForeignKey(User, related_name="updated_by", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'dt_threads'
        verbose_name_plural = 'Thread'

    def __str__(self):
        return self.title


class SubThread(models.Model):
    """Sub Thread Model"""
    thread      =  models.ForeignKey(Thread, on_delete=models.CASCADE)
    view_id     =  models.CharField(max_length=10, blank=False, null=False)
    title       =  models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'dt_sub_threads'
        verbose_name_plural = 'Sub Threads'

    def __str__(self):
        return self.title    


class ThreadLink(models.Model):
    """Thread Link Model"""
    thread      =  models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread')
    sub_thread  =  models.ForeignKey(SubThread, on_delete=models.SET_NULL, blank=True, null=True)
    link        =  models.ForeignKey(Thread, on_delete=models.SET_NULL, related_name='link', blank=True, null=True)

    class Meta:
        db_table = 'dt_thread_links'
        verbose_name_plural = 'Thread Links'     


class ThreadSession(models.Model):
    """Thread Session Model"""
    CHANNEL_OPTIONS = (
        ('WHATSAPP', 'Whatsapp'),
        ('TELEGRAM', 'Telegram'),
    )

    uuid        =  models.CharField(max_length=100, blank=True, null=True)
    phone       =  models.CharField(max_length=20, blank=True, null=True)
    channel     =  models.CharField(max_length=50, choices=CHANNEL_OPTIONS, blank=False, null=False, default='WHATSAPP')  
    thread      =  models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    flag        =  models.CharField(max_length=100, blank=True, null=True)
    values      =  models.TextField(blank=True, null=True)
    active      =  models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'dt_thread_sessions'
        verbose_name_plural = 'Thread Sessions' 
