from django.contrib import admin
from django.shortcuts import render
from import_export.admin import ImportExportModelAdmin
from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'country', 'twitter', 'discord', 'telegram')
