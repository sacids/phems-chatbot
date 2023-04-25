from django.contrib import admin
from .models import *

# Register your models here.
class DistrictInline(admin.TabularInline):
    model = District
    extra = 0

class WardInline(admin.TabularInline):
    model = Ward
    extra = 0

class VillageInline(admin.TabularInline):
    model = Village
    extra = 0

class HamletInline(admin.TabularInline):
    model = Hamlet
    extra = 0


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name__startwith']
    ordering = ("id",)
    inlines  = [DistrictInline]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region']
    search_fields = ['name__startwith']
    ordering = ("id",)
    inlines  = [WardInline]


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dictionary', 'district']
    search_fields = ['name__startwith']
    ordering = ("id",)
    inlines  = [VillageInline]

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dictionary', 'ward']
    search_fields = ['name__startwith']
    ordering = ("id",)
    inlines  = [HamletInline]
