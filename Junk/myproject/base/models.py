from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    username=models.CharField(max_length=256)
    uid = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         unique=True,
         editable = False)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='items_images/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name