from django.contrib import admin
from .models import Remove, PileUp

class RemoveAdmin(admin.ModelAdmin):
    list_display = ['number']

class PileUpAdmin(admin.ModelAdmin):
    list_display = ['number']

admin.site.register(Remove, RemoveAdmin)
admin.site.register(PileUp, PileUpAdmin)
