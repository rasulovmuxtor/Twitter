from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=160,null=True,blank=True)
    website = models.URLField(null=True,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    def __str__(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        return self.username
    def get_absolute_url(self):
        return reverse('user_profile', args=[self.username])        
    def liked(self):
        return self.likes.all().values_list('post',flat=True)
    