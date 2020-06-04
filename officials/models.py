from django.db import models
from institute.models import Blocks, Officials

# Create your models here.
class WaterCan(models.Model):

    date = models.DateField(null=False)
    block = models.ForeignKey(Blocks,on_delete=models.CASCADE, null=False)
    received = models.IntegerField(null=False)
    given = models.IntegerField(null=False)

    def __str__(self):
        return str(self.block.block_id)+','+str(self.date)

