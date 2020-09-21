from django.db import models
from institute.models import Student, Official
from workers.models import Worker

# Create your models here.
class Complaint(models.Model):
    TYPE = (
        ('General','General'),
        ('Food Issues', 'Food Issues'),
        ('Electrical','Electrical'),
        ('Civil', 'Civil'),
        ('Room Cleaning','Room Cleaning'),
        ('Restroom Cleaning','Restroom Cleaning'),
        ('Indisciplinary','Indisciplinary'),
        ('Discrimination/ Harassment','Discrimination/ Harassment'),
        ('Damage to property','Damage to property')
    )
    STATUS = (
        ('Registered','Registered'),
        ('Processing','Processing'),
        ('Resolved','Resolved')
    )
    ENTITY_TYPE = (
        ('Student', 'Student'),
        ('Official', 'Official'),
        ('Worker', 'Worker')
    )

    entity_type = models.CharField(max_length=40, choices=ENTITY_TYPE, null=False)
    entity_id = models.IntegerField()
    type = models.CharField(max_length=40,choices=TYPE, null=False)
    complainee = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True, blank=True)
    
    def entity(self):
        if self.entity_type == 'Student':
            return Student.objects.get(regd_no = self.entity_id)
        elif self.entity_type == 'Official':
            return Official.objects.get(emp_id = self.entity_id)
        else:
            return Worker.objects.get(emp_id = self.entity_id)

    def can_edit(self, user):
        if user.is_official and user.official.is_chief():
            return True
        elif user.is_official and ((self.entity_type != 'Student' and self.entity().block == user.official.block) or self.entity().roomdetail.block == user.official.block):
            return True
        elif user.is_worker:
            return True

        return False

    def model_name(self):
        return "Complaint"

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True, blank=True)

    def entity(self):
        if self.entity_type == 'Student':
            return Student.objects.get(regd_no = self.entity_id)
        elif self.entity_type == 'Official':
            return Official.objects.get(emp_id = self.entity_id)
        else:
            return Worker.objects.get(emp_id = self.entity_id)

    def can_edit(self, user):
        if user.is_worker and user.worker.designation == 'Doctor':
            return True
        return False

    def model_name(self):
        return "Medical Issue"