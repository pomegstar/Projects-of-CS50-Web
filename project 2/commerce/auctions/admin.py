from django.contrib import admin
from .models import User, Category, A_listing, Comments, Bids
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(A_listing)
admin.site.register(Comments)
admin.site.register(Bids)
