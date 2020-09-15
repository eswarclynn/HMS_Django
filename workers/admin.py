from django.contrib import admin
from workers.models import Worker, MedicalIssue, Attendance

# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'name', 'user', 'designation', 'block')

class MedicalIssueAdmin(admin.ModelAdmin):
    list_display = ('entity_id', 'entity_type', 'status', 'summary')

admin.site.register(Worker, WorkerAdmin)
admin.site.register(MedicalIssue, MedicalIssueAdmin)
admin.site.register(Attendance)
