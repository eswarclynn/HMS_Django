from django.contrib import admin
from .models import *

# Register your models here.
class complaintsAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'type', 'summary', 'status', 'date', 'remark')

class officialComplaintsAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'type', 'summary', 'status', 'date', 'remark')

admin.site.register(OfficialComplaints, complaintsAdmin)
admin.site.register(Complaints, officialComplaintsAdmin)