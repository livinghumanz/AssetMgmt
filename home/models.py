from datetime import datetime
from django.db import models

# -------------- Asset list table -----------
class Asset(models.Model):
    asset_id = models.CharField(primary_key=True,max_length=10)
    asset_name = models.CharField(max_length=25)
    asset_description = models.CharField(max_length=40)
    base_location = models.CharField(max_length=20)

    def __str__(self):
        return '{0} | {1}'.format(self.asset_id,self.asset_name)

# -------------- Employee/Holder list table -----------
class Employee(models.Model):
    emp_id = models.CharField(primary_key=True,max_length=10)
    emp_name = models.CharField(max_length=25)
    contact = models.CharField(null=False,max_length=15)
    work_location = models.CharField(max_length=20)

    def __str__(self):
        return '{0} | {1}'.format(self.emp_id,self.emp_name)

# -------------- Asset in and out list table -----------
class In_Out_log(models.Model):
    asset = models.ForeignKey(Asset,on_delete=models.DO_NOTHING)
    emp = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    checkin_date = models.DateTimeField(null=False)
    return_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        if self.return_date == None:
            return '{0} holds {1} from {2}'.format(self.emp.emp_id,self.asset.asset_id,self.checkin_date)
        else:
            return '{0} returned {1} on {2}'.format(self.emp.emp_id,self.asset.asset_id,self.return_date)