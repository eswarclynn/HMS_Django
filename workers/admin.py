from django.contrib import admin
from workers.models import Workers,Medical,attendance

# Register your models here.
admin.site.register(Workers)
admin.site.register(Medical)
admin.site.register(attendance)
