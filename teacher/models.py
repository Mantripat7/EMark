from django.db import models

class students_detials(models.Model):
    fullname = models.CharField(max_length=100)
    roll_no = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    password = models.CharField(max_length=100)
    mst_1_marks = models.IntegerField(blank=True,null=True)
    mst_2_marks = models.IntegerField(blank=True,null=True)
    assignment_1_marks = models.IntegerField(blank=True,null=True)
    assignment_2_marks = models.IntegerField(blank=True,null=True)
    assignment_3_marks = models.IntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='media/images')
    subject = models.CharField(max_length=100,default="")

class attendence(models.Model):
      roll_no = models.IntegerField()
      fullname = models.CharField(max_length=100) 
      date = models.DateField(auto_now_add=True)
      attend = models.CharField(max_length=100 )
      subject = models.CharField(max_length=100,default="")

