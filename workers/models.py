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
    staff_id = models.CharField(unique=True, null=False, max_length=20)
    name = models.CharField(max_length=100, null=False)
    designation = models.CharField(max_length=50,choices=EMP)
    gender = models.CharField(max_length=10,choices=GENDER)
    phone = models.CharField(max_length=12,null=False)
    email = models.EmailField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.staff_id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Attendance.objects.filter(worker = self).exists():
            att = Attendance.objects.create(worker = self)


class MedicalIssue(models.Model):
    STATUS = (
        ('Registered','Registered'),
        ('Resolved','Resolved')
    )
    ENTITY_TYPE = (
        ('Student', 'Student'),
        ('Official', 'Official'),
        ('Worker', 'Worker')
    )

    entity_type = models.CharField(max_length=40, choices=ENTITY_TYPE, null=False)
    entity_id = models.IntegerField()
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    remarks = models.TextField(null=True, blank=True)


class Attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    worker = models.OneToOneField(
        Worker,
        on_delete=models.CASCADE,
    )
    dates = models.TextField(blank=True)
    status = models.CharField(max_length=10,default='',blank=True)

    def __str__(self):
        return str(self.worker.staff_id)