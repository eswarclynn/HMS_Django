from django.contrib import admin
from .models import Institutestd,Officials
from institute.models import Blocks

# Register your models here.
admin.site.register(Institutestd)
admin.site.register(Officials)
admin.site.register(Blocks)