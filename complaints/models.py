from django.db import models
from institute.models import Institutestd, Officials

# Create your models here.
class Complaints(models.Model):
    TYPE = (
        ('General','General'),
        ('Food Issues', 'Food Issues'),
        ('Electrical','Electrical'),
        ('Civil', 'Civil'),
        ('Room Cleaning','Room Cleaning'),
        ('Restroom Cleaning','Restroom Cleaning'),
        ('Indisciplinary','Indisciplinary'),
        ('Discrimination/Harassment','Discrimination/Harassment'),
        ('Damage to property','Damage to property')
    )
    STATUS = (
        ('Registered','Registered'),
        ('Processing','Processing'),
        ('Resolved','Resolved')
    )
    regd_no = models.ForeignKey(Institutestd, on_delete=models.CASCADE, null=False, related_name='complaints')
    type = models.CharField(max_length=40,choices=TYPE, null=False)
    complainee = models.ForeignKey(Institutestd, on_delete=models.CASCADE, null=True, related_name='complainee', blank=True)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    date = models.DateField(auto_now_add=True)

class OfficialComplaints(models.Model):
    TYPE = (
        ('General','General'),
        ('Food Issues', 'Food Issues'),
        ('Electrical','Electrical'),
        ('Civil', 'Civil'),
        ('Room Cleaning','Room Cleaning'),
        ('Restroom Cleaning','Restroom Cleaning'),
        ('Indisciplinary','Indisciplinary'),
        ('Discrimination/Harassment','Discrimination/Harassment'),
        ('Damage to property','Damage to property'),
        ('Latecomer','Latecomer')
    )
    STATUS = (
        ('Registered','Registered'),
        ('Processing','Processing'),
        ('Resolved','Resolved')
    )
    regd_no = models.ForeignKey(Officials, on_delete=models.CASCADE, null=False, related_name='offComplaints')
    type = models.CharField(max_length=40,choices=TYPE, null=False)
    complainee = models.ForeignKey(Institutestd, on_delete=models.CASCADE, null=True, related_name='offComplainee', blank=True)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    date = models.DateField(auto_now_add=True)
