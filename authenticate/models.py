from django.db import models
from institute.models import Institutestd, Officials

# Create your models here.

class credentials(models.Model):
    regd_no = models.ForeignKey(Institutestd, on_delete=models.CASCADE, null=True)
    emp_id = models.ForeignKey(Officials,on_delete=models.CASCADE, null=True)
    password = models.CharField(max_length=25,null=False)

    class Meta:
        unique_together = (("regd_no", "emp_id"),)