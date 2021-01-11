from institute.models import Student
from django.db.models.signals import post_save
from django.dispatch import receiver
from students.models import RoomDetail, Attendance, Document, FeeDetail

@receiver(post_save, sender=Student)
def create_student_dependencies(sender, instance, created, **kwargs):
    if instance.is_hosteller:
        if not RoomDetail.objects.filter(student = instance).exists():
            RoomDetail.objects.create(student=instance)
        if not Attendance.objects.filter(student = instance).exists():
            Attendance.objects.create(student=instance)
        if not Document.objects.filter(student = instance).exists():
            Document.objects.create(student = instance)
        if not FeeDetail.objects.filter(student = instance).exists():
            FeeDetail.objects.create(student = instance)
