from django.db import models

class sumanmodel(models.Model):
    
    file=models.FileField(upload_to='Documents/')
    filename=models.CharField(max_length=100,null=False,blank=True)
    upload_date = models.DateField(auto_now_add=True,blank=True)
    upload_time = models.TimeField(auto_now_add=True,blank=True)
    textdata=models.TextField(blank=True)   
    



#'%d-%m-%Y %H:%M:%S'