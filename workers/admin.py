from django.contrib import admin
from workers.models import Workers,Medical,attendance

# Register your models here.
class workersAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'name', 'designation', 'block')

class medicalAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'status', 'summary')

admin.site.register(Workers, workersAdmin)
admin.site.register(Medical, medicalAdmin)
admin.site.register(attendance)
