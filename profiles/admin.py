from django.contrib import admin

from .models import HistoryNovel, Profile,History
# Register your models here.

admin.site.register(Profile)
admin.site.register(History)
admin.site.register(HistoryNovel)



