from django.contrib import admin
from .models import Student, Official, Block

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'name', 'user', 'roll_no', 'year', 'branch','gender', 'phone')

class OfficialAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'user', 'designation', 'phone', 'block')

class BlocksAdmin(admin.ModelAdmin):
    list_display = ('name', 'block_id', 'room_type', 'gender', 'capacity')

admin.site.register(Student, StudentAdmin)
admin.site.register(Official, OfficialAdmin)
admin.site.register(Block, BlocksAdmin)