import random
from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    mobile = models.IntegerField()
    register_id = models.CharField(max_length=100, blank=True, unique=True, editable=True)

    def save(self, *args, **kwargs):
        self.register_id = "ST" + str(random.randint(100000, 999999))
        return super().save(*args, **kwargs)