from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(PowerPlant)
class PowerPlantAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PowerPlant._meta.fields]
    search_fields = [f.name for f in PowerPlant._meta.fields]

@admin.register(DemandLocation)
class DemandLocationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DemandLocation._meta.fields]
    search_fields = [f.name for f in DemandLocation._meta.fields]

@admin.register(DistBtoD)
class DistBtoDAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DistBtoD._meta.fields]
    search_fields = [f.name for f in DistBtoD._meta.fields]

@admin.register(DistBtoP)
class DistBtoPAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DistBtoP._meta.fields]
    search_fields = [f.name for f in DistBtoP._meta.fields]

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Block._meta.fields]
    search_fields = [f.name for f in Block._meta.fields]