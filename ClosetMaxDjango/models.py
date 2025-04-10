from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# User Model
# In your app's models.py file

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)  # Phone number field

    # Override the reverse relationships with a unique related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Use a custom related_name to avoid clashes
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Custom related_name for permissions
        blank=True,
    )

    class Meta:
        db_table = 'CustomModel'  # Specify a custom table name (optional)


# Closet model
class Closet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='closets')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Closet'

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# Clothes Model
class Clothes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Reference User model directly
    closet = models.ForeignKey(Closet, on_delete=models.CASCADE, related_name='clothes', null=True, blank=True)
    material = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)

    
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'),
        ('XXL', 'XXL'), ('32', '32'), ('34', '34'), ('36', '36'), ('38', '38')
    ]
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, null=True, blank=True)

    SEASON_CHOICES = [
        ('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall'), ('Winter', 'Winter')
    ]
    season = models.CharField(max_length=255, null=True, blank=True, choices=SEASON_CHOICES)
    
    brand = models.CharField(max_length=255, null=True, blank=True)
    clothing_type = models.CharField(max_length=255, null=True, blank=True)
    favorite = models.BigIntegerField(null=True, blank=True)  
    date_added = models.DateTimeField(null=True, blank=True, auto_now=True)
    image = models.ImageField(upload_to='clothes_images/', null=True, blank=True)

    class Meta:
        db_table = 'Clothes'

    def __str__(self):
        return f"{self.material} - {self.size}" if self.material and self.size else "Clothing Item"

