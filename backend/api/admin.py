from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Story)
admin.site.register(StoryLine)
admin.site.register(Genre)
admin.site.register(ProfilePicture)