from django.contrib import admin
from .models import Complaint, MedicalIssue

# Register your models here.
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('entity_id', 'entity_type', 'type', 'summary', 'status', 'created_at', 'updated_at', 'remark')

class MedicalIssueAdmin(admin.ModelAdmin):
    list_display = ('entity_id', 'entity_type', 'status', 'summary')

admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(MedicalIssue, MedicalIssueAdmin)