from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

# Create your models here.

class Garbage(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    cpassword=models.CharField(max_length=30)
    
    def __str__(self):  
        return self.username

    
def validate_phone_number(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('Phone number must be exactly 10 digits.')

class Contact(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    message=models.TextField()
    phone = models.CharField(
        max_length=10, 
        validators=[validate_phone_number],
        help_text='Enter a 10-digit phone number')

    def __str__(self):  
        return self.name


class Plant(models.Model):
    pname=models.CharField(max_length=50)
    desc=models.TextField()

    def __str__(self):
        return self.pname

    
class Booking(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    place = models.CharField(max_length=50)
    waste_type = models.CharField(
        max_length=20,
        choices=[
            ('bio-degradable', 'Bio-degradable'),
            ('non-biodegradable', 'Non-biodegradable'),
            ('hazardous', 'Hazardous'),
        ]
    )
    weight = models.PositiveIntegerField()  
    date = models.DateField()
    time = models.TimeField()
    selected_plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.date} - {self.selected_plant.pname if self.selected_plant else "No plant selected"}'


class PasswordResetToken(models.Model):
    user = models.ForeignKey(Garbage, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)  #universally unique identifier (UUID) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def is_token_valid(self):
        # Check if the token is still valid (e.g., valid for 1 hour)
        return self.is_active and (timezone.now() - self.created_at).total_seconds() < 3600

    def __str__(self):
        return f"{self.user.username}"


