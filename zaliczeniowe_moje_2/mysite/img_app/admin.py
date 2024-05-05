from django.contrib import admin
from .models import Tag, Image

admin.site.register(Image)
admin.site.register(Tag)