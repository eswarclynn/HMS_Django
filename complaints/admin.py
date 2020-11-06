from django.contrib import admin
from .models import Complaint, MedicalIssue

# Register your models here.
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('entity', 'type', 'summary', 'status', 'created_at', 'updated_at', 'remark')

class MedicalIssueAdmin(admin.ModelAdmin):
    list_display = ('entity', 'status', 'summary')

admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(MedicalIssue, MedicalIssueAdmin)