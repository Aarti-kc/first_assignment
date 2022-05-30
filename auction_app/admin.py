from django.contrib import admin
from auction_app.models import *

from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(Products)
admin.site.register(Bidding)
admin.site.register(Comments)
admin.site.register(Watchlist)


admin.site.register(User, UserAdmin)