from django.contrib import admin
from students.models import details,attendance,outing

# Register your models here.
admin.site.register(details)
admin.site.register(attendance)
admin.site.register(outing)