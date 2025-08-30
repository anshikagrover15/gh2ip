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

@admin.register(DistBtoDTable)
class DistBtoDAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DistBtoDTable._meta.fields]
    search_fields = [f.name for f in DistBtoDTable._meta.fields]

@admin.register(DistBtoPTable)
class DistBtoPAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DistBtoPTable._meta.fields]
    search_fields = [f.name for f in DistBtoPTable._meta.fields]

@admin.register(BlockTable)
class BlockAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BlockTable._meta.fields]
    search_fields = [f.name for f in BlockTable._meta.fields]