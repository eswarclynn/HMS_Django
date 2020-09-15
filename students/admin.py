from django.contrib import admin
from students.models import RoomDetail,Attendance,Outing

# Register your models here.
class RoomDetailAdmin(admin.ModelAdmin):
    list_display = ('student', 'block', 'room_no', 'floor')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'status')

class OutingAdmin(admin.ModelAdmin):
    list_display = ('student', 'fromDate', 'fromTime', 'toDate', 'toTime', 'purpose', 'permission')

admin.site.register(RoomDetail, RoomDetailAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Outing, OutingAdmin)