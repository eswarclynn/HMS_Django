from django.contrib import admin
from .models import Complaint

# Register your models here.
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('entity_id', 'entity_type', 'type', 'summary', 'status', 'created_at', 'updated_at', 'remark')

admin.site.register(Complaint, ComplaintAdmin)