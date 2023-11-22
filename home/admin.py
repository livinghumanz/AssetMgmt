from django.contrib import admin

# Register your models here.

from .models import Asset,Employee,In_Out_log

# Register your models here.
admin.site.register([Asset,Employee,In_Out_log])