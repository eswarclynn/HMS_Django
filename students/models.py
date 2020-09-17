from django.db import models

# Create your models here.
class RoomDetail(models.Model):
    FLOOR_OPTIONS = (
        ('Ground', 'Ground'),
        ('First', 'First'),
        ('Second', 'Second')
    )

    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    block = models.ForeignKey('institute.Block', on_delete=models.CASCADE, null=True, blank=True)
    room_no = models.IntegerField(null=True, blank=True)
    floor = models.CharField(max_length=10, choices=FLOOR_OPTIONS, null=True, blank=True)

    def __str__(self):
        block = self.block_id or "None"
        floor = self.floor or "None"
        return "{regd_no}<{block}: {floor}-{room}>".format(
            regd_no = self.student, 
            block = block,
            floor = floor,
            room = self.room_no or 0
        )

class Attendance(models.Model):
    OPTIONS = (
        ('Present','Present'),
        ('Absent','Absent')
    )
    student = models.OneToOneField('institute.Student', on_delete=models.CASCADE, null=False)
    dates = models.TextField()
    status = models.CharField(max_length=10,default='')

    def __str__(self):
        return str(self.student)

class Outing(models.Model):
    PERMIT_OPTIONS = (
        ('Pending','Pending'),
        ('Granted', 'Granted'),
        ('Rejected', 'Rejected')
    )

    student = models.ForeignKey('institute.Student', on_delete=models.CASCADE, null=False)
    fromDate = models.DateField(null=False)
    fromTime = models.TimeField(null=False)
    toDate = models.DateField(null=False)
    toTime = models.TimeField(null=False)
    purpose = models.CharField(max_length=150, null=False)
    permission = models.CharField(max_length=20, choices=PERMIT_OPTIONS, default='Pending', null=False)
