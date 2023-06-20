from django.contrib import admin
from .models import Users, Items, CloudFiles, Folder, News

admin.site.register(Users)
admin.site.register(Items)
admin.site.register(CloudFiles)
admin.site.register(Folder)
admin.site.register(News)
