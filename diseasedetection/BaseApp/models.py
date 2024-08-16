from django.db import models
import os

# Define the Login table
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=10)
    id = models.AutoField(primary_key=True)

    # def __str__(self):
    #     return self.username


# Define the Staff table
class Staff(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    log_id = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)


    # def __str__(self):
    #     return self.name


# Define the Doctor table
class Doctor(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    log_id = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    id = models.AutoField(primary_key=True)

    # def __str__(self):
    #     return self.name

# Define the PatientData table
class PatientData(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    fmri_photo = models.ImageField(upload_to='fmri_photos/')
    datetime = models.DateTimeField(auto_now_add=True, null=True)    
    # log_id = models.OneToOneField(Login, on_delete=models.CASCADE, primary_key=True)

    # def __str__(self):
    #     return self.name
