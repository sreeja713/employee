from django.db import models

class Employee(models.Model):
    Name = models.CharField(max_length = 255, blank=False)
    Email = models.EmailField(blank=False, unique=True, max_length= 255)
    Photo = models.ImageField(upload_to='images', blank=True, null=True)