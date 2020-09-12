from django.db import models
from students.models import details, attendance

# Create your models here.
class Institutestd (models.Model):
    YEAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    BRANCH=(
        ('CSE','Computer Science Engineering'),
        ('ECE','Electronic and Communication Engineering'),
        ('EEE','Electrical and Electronic Engineering'),
        ('CHE','Chemical Engineering'),
        ('MME','Metalurgy Engineering'),
        ('MEC','Mechanical Engineering'),
        ('CIV','Civil Engineering'),
        ('BIO','Bio Technology'),
    )
    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
    )
    CASTE = (
        ('GEN', 'GEN'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('EWS', 'EWS')
    )

    regd_no = models.IntegerField(primary_key=True,null=False)
    roll_no = models.IntegerField(null=False)
    name = models.CharField(max_length=100,null=False)
    email_id = models.CharField(max_length=50,null=False, unique=True)
    branch = models.CharField(max_length=3,choices=BRANCH,null=False)
    gender = models.CharField(max_length=7,choices=GENDER,null=False)
    pwd = models.BooleanField(null=False, default=False)
    community = models.CharField(max_length=25, choices=CASTE, null=False, default='GEN')
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

        if not details.objects.filter(regd_no = self).exists():
            det = details.objects.create(regd_no=self)
        if not attendance.objects.filter(regd_no = self).exists():
            att = attendance.objects.create(regd_no=self)


class Officials (models.Model):
    EMP=(
        ('Caretaker','Caretaker'),
        ('Warden','Warden'),
        ('Deputy Chief-Warden', 'Deputy Chief-Warden'),
        ('Chief-Warden','Chief-Warden'),

    )
    BRANCHES=(
        ('CSE','Computer Science Engineering'),
        ('ECE','Electronic and Communication Engineering'),
        ('EEE','Electrical and Electronic Engineering'),
        ('CHE','Chemical Engineering'),
        ('MME','Metalurgy Engineering'),
        ('MEC','Mechanical Engineering'),
        ('CIV','Civil Engineering'),
        ('BIO','Bio Technology'),

    )

    emp_id = models.IntegerField(primary_key=True,null=False)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=20,choices=EMP)
    branch=models.CharField(max_length=20,choices=BRANCHES,default="CSE")
    phone = models.CharField(max_length=10, null=False)
    email_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.emp_id)


class Blocks (models.Model):
    OPTION=(
          ('1S','One student per Room'),
          ('2S','Two students per Room'),
          ('4S','Four students per Room'),
     )

    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
     )

    emp_id = models.OneToOneField(
        Officials,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    block_id = models.IntegerField(primary_key=True)
    block_name=models.CharField(max_length=50,null=False)
    room_type=models.CharField(max_length=2,choices=OPTION)
    gender = models.CharField(max_length=7,choices=GENDER)
    capacity = models.IntegerField(null=False)
