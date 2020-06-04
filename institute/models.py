from django.db import models

# Create your models here.
class Institutestd (models.Model):
    OPTION = (
        ('Y', 'Yes'),
        ('N', 'No'),
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
    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
    )

    regd_no = models.IntegerField(primary_key=True,null=False)
    roll_no = models.IntegerField(null=False)
    name = models.CharField(max_length=100,null=False)
    branch = models.CharField(max_length=3,choices=BRANCHES,null=False)
    gender = models.CharField(max_length=7,choices=GENDER,null=False)
    pwd = models.CharField(max_length=5,choices=OPTION,null=False)
    caste = models.CharField(max_length=25,null=False)
    year = models.IntegerField(null=False)
    dob = models.DateField(null=False)
    bgp = models.CharField(max_length=25,null=False)
    email_id = models.CharField(max_length=50,null=False)
    phone = models.CharField(null=False, max_length=10)
    ph_phone = models.CharField(null=False, max_length=10)
    emr_phone = models.CharField(null=False, max_length=10)
    address = models.CharField(max_length=100,null=False)
    photo = models.FileField(null=True, blank=True)
    hosteller = models.CharField(max_length=1, choices=OPTION ,null=False)
    amount = models.IntegerField(null=True, blank=True,default=0)
    bank = models.CharField(max_length=100,null=True, blank=True)
    ch_no = models.CharField(max_length=64,null=True, blank=True)
    dop = models.DateField(null=True, blank=True)
    application = models.FileField(null=True, blank=True)
    undertake = models.FileField(null=True, blank=True)
    recipt = models.FileField(null=True, blank=True)
    afd = models.FileField(null=True, blank=True)
    paid = models.CharField(max_length=1,choices=OPTION ,null=False)

    def __str__(self):
        return str(self.regd_no)


class Officials (models.Model):
    EMP=(
        ('Caretaker','Caretaker'),
        ('Warden','Warden'),
        ('Deputy Chief-Warden', 'Deputy Chief-Warden'),
        ('Chief-Warden','ChiefWarden'),

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
    email_id = models.CharField(max_length=50)

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
