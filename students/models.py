from django.db import models
from django.db.models.base import Model
from django.utils import timezone

# Create your models here.
class RoomDetail(models.Model):
    FLOOR_OPTIONS = (
        ('Ground', 'Ground'),
        ('First', 'First'),
        ('Second', 'Second')
    )

    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    block = models.ForeignKey('institute.Block', on_delete=models.CASCADE, null=True, blank=True)
    room_no = models.IntegerField(null=True, blank=True)
    floor = models.CharField(max_length=10, choices=FLOOR_OPTIONS, null=True, blank=True)

    def __str__(self):
        block = self.block_id or "None"
        floor = self.floor or "None"
        return "{regd_no}<{block}: {floor}-{room}>".format(
            regd_no = self.student, 
            block = block,
            floor = floor[0],
            room = self.room_no or 0
        )

    def room(self):
        return self.floor and self.room_no and "{}-{}".format(self.floor[0], self.room_no)

class Attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    present_dates = models.TextField(null=True, blank=True)
    absent_dates = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.student)

    def mark_attendance(self, date, status):
        if status == 'present':
            absent_dates = self.absent_dates and set(self.absent_dates.split(',')) or set()
            absent_dates.discard(date)
            self.absent_dates = ','.join(absent_dates)
            if not self.present_dates: 
                self.present_dates = date
            else:
                self.present_dates = ','.join(set(self.present_dates.split(',') + [date]))
        elif status == 'absent':
            present_dates = self.present_dates and set(self.present_dates.split(',')) or set()
            present_dates.discard(date)
            self.present_dates = ','.join(present_dates)
            if not self.absent_dates: 
                self.absent_dates = date
            else:
                self.absent_dates = ','.join(set(self.absent_dates.split(',') + [date]))

        self.save()
        
class Outing(models.Model):
    PERMIT_OPTIONS = (
        ('Pending','Pending'),
        ('Granted', 'Granted'),
        ('Rejected', 'Rejected')
    )

    student = models.ForeignKey('institute.Student', on_delete=models.CASCADE, null=False)
    fromDate = models.DateTimeField(null=False)
    toDate = models.DateTimeField(null=False)
    purpose = models.CharField(max_length=150, null=False)
    permission = models.CharField(max_length=20, choices=PERMIT_OPTIONS, default='Pending', null=False)

    def is_upcoming(self):
        return self.fromDate > timezone.now()

    def is_editable(self):
        return self.is_upcoming() and self.permission == 'Pending'

    class Meta:
        ordering = ['-fromDate']

class Document(models.Model):
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    application = models.FileField(null=True, blank=True)
    undertaking_form = models.FileField(null=True, blank=True)
    receipt = models.FileField(null=True, blank=True)
    day_scholar_affidavit = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return 'Document: {} - {}'.format(self.id, self.student.regd_no)

class FeeDetail(models.Model):
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    has_paid = models.BooleanField(null=True, default=False)
    amount_paid = models.FloatField(null=True, blank=True,default=0)
    bank = models.CharField(max_length=100,null=True, blank=True)
    challan_no = models.CharField(max_length=64,null=True, blank=True)
    dop = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return 'Bank Detail: {} - {}'.format(self.id, self.student.regd_no)
