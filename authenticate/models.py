from django.db import models
from institute.models import Institutestd, Officials
from workers.models import Workers

# Create your models here.

class credentials(models.Model):
    regd_no = models.ForeignKey(Institutestd, on_delete=models.CASCADE, null=True, blank=True)
    emp_id = models.ForeignKey(Officials,on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(Workers,on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=25,null=False)

    class Meta:
        unique_together = (("regd_no", "emp_id", "staff_id"),)

    def __str__(self):
        if self.regd_no:
            return str(self.regd_no)
        elif self.emp_id:
            return str(self.emp_id)
        elif self.staff_id:
            return str(self.staff_id)
