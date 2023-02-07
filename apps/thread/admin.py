from django.contrib import admin
from .models import *

# Register your models here.
class SubThreadInline(admin.TabularInline):
    model = SubThread
    extra = 0


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'flag']
    search_fields = ['title__startwith']
    ordering = ("id",)
    inlines  = [SubThreadInline]


# @admin.register(ThreadLink)
# class ThreadLinkAdmin(admin.ModelAdmin):
#     list_display = ['id', 'thread', 'sub_thread', 'link']
#     ordering = ("id",)
