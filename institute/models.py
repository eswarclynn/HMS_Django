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
    pwd = models.CharField(max_length=1,choices=OPTION,null=False)
    phone = models.IntegerField(null=False)
    address = models.CharField(max_length=100,null=False)
    year = models.IntegerField(null=False)
    email_id = models.CharField(max_length=50,null=False)
    dob = models.DateField(null=False)
    hosteller = models.CharField(max_length=1, choices=OPTION ,null=False)
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

    emp_id = models.IntegerField(primary_key=True,null=False)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=20,choices=EMP)
    address = models.CharField(max_length=100)
    phone = models.IntegerField(null=False)
    email_id = models.CharField(max_length=50)

    def __str__(self):
        return str(self.emp_id)


class Blocks (models.Model):
    OPTION=(
          ('1S','One student per Room'),
          ('2S','Two students per Room'),
          ('3S','Three students per Room'),
     )

    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
     )

    emp_id = models.OneToOneField(
        Officials,
        on_delete=models.CASCADE,
        null=False
    )
    block_id = models.IntegerField(primary_key=True)
    block_name=models.CharField(max_length=50,null=False)
    room_type=models.CharField(max_length=2,choices=OPTION)
    gender = models.CharField(max_length=7,choices=GENDER)
    capacity = models.IntegerField(null=False)
