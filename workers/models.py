from django.db import models
from institute.models import Blocks

# Create your models here.
class Workers(models.Model):
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

    staff_id = models.IntegerField(primary_key=True,null=False)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50,choices=EMP)
    gender=models.CharField(max_length=10,choices=GENDER,default="Male")
    phone = models.CharField(max_length=12,null=False)
    email_id = models.CharField(max_length=50, unique=True)
    block = models.ForeignKey(Blocks, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.staff_id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not attendance.objects.filter(worker = self).exists():
            att = attendance.objects.create(worker = self)


class Medical(models.Model):
    STATUS = (
        ('Registered','Registered'),
        ('Resolved','Resolved')
    )

    regd_no = models.CharField(max_length=10,null=False)
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    remarks = models.TextField(null=True, blank=True)


class attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    worker = models.OneToOneField(
        Workers,
        on_delete=models.CASCADE,
    )
    dates = models.TextField(blank=True)
    status = models.CharField(max_length=10,default='',blank=True)

    def __str__(self):
        return str(self.staff_id)