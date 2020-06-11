from django.contrib import admin
from .models import Institutestd,Officials
from institute.models import Blocks

# Register your models here.
class InstitutestdAdmin(admin.ModelAdmin):
    list_display = ('regd_no', 'roll_no', 'name', 'year', 'branch','gender', 'phone')

class OfficialsAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'designation', 'branch', 'phone')

class BlocksAdmin(admin.ModelAdmin):
    list_display = ('block_id', 'block_name', 'room_type', 'gender', 'capacity')

admin.site.register(Institutestd, InstitutestdAdmin)
admin.site.register(Officials, OfficialsAdmin)
admin.site.register(Blocks, BlocksAdmin)