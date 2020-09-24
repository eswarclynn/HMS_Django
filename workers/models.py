from django.db import models
from django.conf import settings
from institute.models import Block

# Create your models here.
class Worker(models.Model):
    EMP=(
        ('Scavenger','Scavenger'),
        ('General Servant','General Servant'),
        ('Doctor', 'Doctor'),
        ('Mess Incharge', 'Mess Incharge'),
        ('Electrician','Electrician'), 
        ('Gym Trainer','Gym Trainer'),
        ('PT/Games Coach','PT/Games Coach'),
    )
    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    account_email = models.EmailField(unique=True, null=False)
    staff_id = models.CharField(unique=True, null=False, max_length=20)
    name = models.CharField(max_length=100, null=False)
    designation = models.CharField(max_length=50,choices=EMP)
    gender = models.CharField(max_length=10,choices=GENDER)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.staff_id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Attendance.objects.filter(worker = self).exists():
            att = Attendance.objects.create(worker = self)


class Attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    worker = models.OneToOneField(
        Worker,
        on_delete=models.CASCADE,
    )
    present_dates = models.TextField(null=True, blank=True)
    absent_dates = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.worker.staff_id)

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