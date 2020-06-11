from django.contrib import admin
from students.models import details,attendance,outing

# Register your models here.
class detailsAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'block_id', 'room_no', 'floor')

class attendanceAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'status')

class outingAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'fromDate', 'fromTime', 'toDate', 'toTime', 'purpose', 'parent_mobile', 'permission')


admin.site.register(details, detailsAdmin)
admin.site.register(attendance, attendanceAdmin)
admin.site.register(outing, outingAdmin)