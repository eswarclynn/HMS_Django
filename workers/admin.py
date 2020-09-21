from django.contrib import admin
from workers.models import Worker, Attendance

# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'name', 'user', 'designation', 'block')



admin.site.register(Worker, WorkerAdmin)
admin.site.register(Attendance)
