from django.contrib import admin
from .models import CustomUser, Invitation

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Invitation)
