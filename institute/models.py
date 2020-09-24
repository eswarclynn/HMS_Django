from django.db import models
from students.models import RoomDetail, Attendance
from django.conf import settings

# Create your models here.
class Student(models.Model):
    YEAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    BRANCH=(
        ('CSE','Computer Science and Engineering'),
        ('ECE','Electronics and Communication Engineering'),
        ('EEE','Electrical and Electronics Engineering'),
        ('CHE','Chemical Engineering'),
        ('MME','Metallurgical and Materials Engineering'),
        ('MEC','Mechanical Engineering'),
        ('CIV','Civil Engineering'),
        ('BIO','Biotechnology'),
    )
    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
    )
    COMMUNITY = (
        ('GEN', 'GEN'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('EWS', 'EWS')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    account_email = models.EmailField(unique=True, null=False)
    regd_no = models.CharField(unique=True, null=False, max_length=20)
    roll_no = models.CharField(unique=True, null=False, max_length=20)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=True, blank=True)
    branch = models.CharField(max_length=3,choices=BRANCH,null=False)
    gender = models.CharField(max_length=7,choices=GENDER,null=False)
    pwd = models.BooleanField(null=False, default=False)
    community = models.CharField(max_length=25, choices=COMMUNITY, null=False)
    year = models.IntegerField(null=False, choices=YEAR)
    dob = models.DateField(null=False)
    blood_group = models.CharField(max_length=25,null=False)
    phone = models.CharField(null=False, max_length=10)
    parents_phone = models.CharField(null=False, max_length=10)
    emergency_phone = models.CharField(null=False, max_length=10)
    address = models.CharField(max_length=100,null=False)
    photo = models.FileField(null=True, blank=True)
    is_hosteller = models.BooleanField(null=False, default=True)
    has_paid = models.BooleanField(null=True, default=False)
    amount_paid = models.FloatField(null=True, blank=True,default=0)
    bank = models.CharField(max_length=100,null=True, blank=True)
    challan_no = models.CharField(max_length=64,null=True, blank=True)
    dop = models.DateField(null=True, blank=True)
    application = models.FileField(null=True, blank=True)
    undertaking_form = models.FileField(null=True, blank=True)
    receipt = models.FileField(null=True, blank=True)
    affidavit = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.regd_no)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not RoomDetail.objects.filter(student = self).exists():
            det = RoomDetail.objects.create(student=self)
        if not Attendance.objects.filter(student = self).exists():
            att = Attendance.objects.create(student=self)


class Official(models.Model):
    EMP=(
        ('Caretaker','Caretaker'),
        ('Warden','Warden'),
        ('Deputy Chief-Warden', 'Deputy Chief-Warden'),
        ('Chief-Warden','Chief-Warden'),

    )
    BRANCH=(
        ('CSE','Computer Science and Engineering'),
        ('ECE','Electronics and Communication Engineering'),
        ('EEE','Electrical and Electronics Engineering'),
        ('CHE','Chemical Engineering'),
        ('MME','Metallurgical and Materials Engineering'),
        ('MEC','Mechanical Engineering'),
        ('CIV','Civil Engineering'),
        ('BIO','Biotechnology'),
        ('SOS', 'School of Sciences'),
        ('SHM', 'School of Humanities and Management')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    account_email = models.EmailField(unique=True, null=False)
    emp_id = models.CharField(unique=True,null=False, max_length=20)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=20,choices=EMP)
    branch=models.CharField(max_length=20,choices=BRANCH)
    phone = models.CharField(max_length=10, null=False)
    email = models.EmailField(null=True, blank=True)
    block = models.ForeignKey('institute.Block', on_delete=models.SET_NULL, null=True, blank=True)

    def is_chief(self):
        return (self.designation == 'Deputy Chief-Warden' or self.designation == 'Chief-Warden')


    def __str__(self):
        return str(self.emp_id)


class Block(models.Model):
    OPTION=(
          ('1S','One student per Room'),
          ('2S','Two students per Room'),
          ('4S','Four students per Room'),
     )

    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
     )

    block_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=50,null=False)
    room_type = models.CharField(max_length=2,choices=OPTION)
    gender = models.CharField(max_length=7,choices=GENDER)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    def short_name(self):
        return self.name.split()[0]

    def student_capacity(self):
        if self.room_type == '4S':   return self.capacity*4
        elif self.room_type == '2S': return self.capacity*2
        elif self.room_type == '1S': return self.capacity

    def students(self):
        return RoomDetail.objects.filter(block=self)

    def caretaker(self):
        return self.official_set.all().first()