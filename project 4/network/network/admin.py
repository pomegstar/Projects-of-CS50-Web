from django.contrib import admin

# Register your models here.
from .models import User, Posts, Follow, Like

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Follow)
admin.site.register(Like)
