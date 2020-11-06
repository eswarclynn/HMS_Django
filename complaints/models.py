from django.contrib.auth import get_user_model
from django.db import models
from institute.models import Student, Official
from workers.models import Worker

User = get_user_model()

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=40,choices=TYPE, null=False)
    complainee = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=True, blank=True)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True, blank=True)
    
    def entity(self):
        return self.user.entity()

    def can_edit(self, user):
        if user.is_official and user.official.is_chief():
            return True
        elif user.is_official and ((self.user.entity_type() != 'Student' and self.entity().block == user.official.block) or self.entity().roomdetail.block == user.official.block):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,null=False,default='Registered',choices=STATUS)
    summary = models.CharField(max_length=200,null=False)
    detailed = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True, blank=True)

    def entity(self):
        return self.user.entity()

    def can_edit(self, user):
        if user.is_worker and user.worker.designation == 'Doctor':
            return True
        return False

    def model_name(self):
        return "Medical Issue"