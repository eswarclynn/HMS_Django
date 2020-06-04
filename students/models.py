from django.db import models
from institute.models import Blocks, Institutestd

# Create your models here.
class details(models.Model):
    FLOOR_OPTIONS = (
        ('Ground', 'Ground'),
        ('First', 'First'),
        ('Second', 'Second')
    )

    regd_no = models.OneToOneField(
        Institutestd,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    block_id = models.ForeignKey(Blocks,on_delete=models.CASCADE, null=True, blank=True)
    room_no = models.IntegerField(null=True, blank=True)
    floor = models.CharField(max_length=10, choices=FLOOR_OPTIONS, null=True, blank=True)

class attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    regd_no = models.OneToOneField(
        Institutestd,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    dates = models.TextField()
    status = models.CharField(max_length=10,default='')

class outing(models.Model):
    PERMIT_OPTIONS = (
        ('Pending','Pending'),
        ('Granted', 'Granted'),
        ('Rejected', 'Rejected')
    )

    regd_no = models.ForeignKey(Institutestd, on_delete=models.CASCADE, null=False)
    fromDate = models.DateField(null=False)
    fromTime = models.TimeField(null=False)
    toDate = models.DateField(null=False)
    toTime = models.TimeField(null=False)
    purpose = models.CharField(max_length=150, null=False)
    parent_mobile = models.BigIntegerField(null=False)
    permission = models.CharField(max_length=20, choices=PERMIT_OPTIONS, default='Pending', null=False)
