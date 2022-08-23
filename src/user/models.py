import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
# Database schemas intilization
class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return str(self.state_id)

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    state = models.ForeignKey(State, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city_id)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    blood_bank_name = models.CharField(max_length=120, blank=False)
    username = models.CharField(max_length=40, unique=True, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    contact = models.CharField(max_length=10, default="N/A", blank=False)
    address = models.CharField(max_length=400, default="N/A", blank=False)
    roles = models.CharField(max_length=20, default="N/A", blank=False) #blood_bank : for role based restriction
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,  default = None)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, default = None)
    
    def __str__(self):
        return str(self.user_id)

class BloodCamp(models.Model):
    camp_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="N/A", null=True, blank=False)
    organizer = models.CharField(max_length=100, default="N/A", null=True, blank=False)
    start_date = models.CharField(max_length=30, default="N/A", null=True, blank=False)
    end_date = models.CharField(max_length=30, default="N/A", null=True, blank=False)
    start_time = models.CharField(max_length=30, default="N/A", null=True, blank=False)
    end_time = models.CharField(max_length=30, default="N/A", null=True, blank=False)
    location = models.CharField(max_length=100, default="N/A", null=True, blank=False)
    description = models.CharField(max_length=400, default="N/A", null=True, blank=False)

    def __str__(self):
        return str(self.camp_id)

class RBC(models.Model):
    rbc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ABpstv = models.IntegerField(default=0, blank=False)
    quantity_ABngtv = models.IntegerField(default=0, blank=False)
    quantity_Apstv = models.IntegerField(default=0, blank=False)
    quantity_Angtv = models.IntegerField(default=0, blank=False)
    quantity_Bpstv = models.IntegerField(default=0, blank=False)
    quantity_Bngtv = models.IntegerField(default=0, blank=False)
    quantity_Opstv = models.IntegerField(default=0, blank=False)
    quantity_Ongtv = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.rbc_id)

class Platelets(models.Model):
    platelets_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ABpstv = models.IntegerField(default=0, blank=False)
    quantity_ABngtv = models.IntegerField(default=0, blank=False)
    quantity_Apstv = models.IntegerField(default=0, blank=False)
    quantity_Angtv = models.IntegerField(default=0, blank=False)
    quantity_Bpstv = models.IntegerField(default=0, blank=False)
    quantity_Bngtv = models.IntegerField(default=0, blank=False)
    quantity_Opstv = models.IntegerField(default=0, blank=False)
    quantity_Ongtv = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.platelets_id)

class Plasma(models.Model):
    plasma_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ABpstv = models.IntegerField(default=0, blank=False)
    quantity_ABngtv = models.IntegerField(default=0, blank=False)
    quantity_Apstv = models.IntegerField(default=0, blank=False)
    quantity_Angtv = models.IntegerField(default=0, blank=False)
    quantity_Bpstv = models.IntegerField(default=0, blank=False)
    quantity_Bngtv = models.IntegerField(default=0, blank=False)
    quantity_Opstv = models.IntegerField(default=0, blank=False)
    quantity_Ongtv = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.plasma_id)

class CryoAHF(models.Model):
    cryo_ahf_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ABpstv = models.IntegerField(default=0, blank=False)
    quantity_ABngtv = models.IntegerField(default=0, blank=False)
    quantity_Apstv = models.IntegerField(default=0, blank=False)
    quantity_Angtv = models.IntegerField(default=0, blank=False)
    quantity_Bpstv = models.IntegerField(default=0, blank=False)
    quantity_Bngtv = models.IntegerField(default=0, blank=False)
    quantity_Opstv = models.IntegerField(default=0, blank=False)
    quantity_Ongtv = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.cryo_ahf_id)

class Granulocytes(models.Model):
    granulocytes_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ABpstv = models.IntegerField(default=0, blank=False)
    quantity_ABngtv = models.IntegerField(default=0, blank=False)
    quantity_Apstv = models.IntegerField(default=0, blank=False)
    quantity_Angtv = models.IntegerField(default=0, blank=False)
    quantity_Bpstv = models.IntegerField(default=0, blank=False)
    quantity_Bngtv = models.IntegerField(default=0, blank=False)
    quantity_Opstv = models.IntegerField(default=0, blank=False)
    quantity_Ongtv = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.granulocytes_id)
