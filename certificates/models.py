from django.db import models

# Create your models here.
from django.db import models

class Participant(models.Model):
    POSITION_CHOICES = [
        ('participant', 'Participant'),
        ('top10', 'Top 10'),
        ('top3', 'Top 3 Winner'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='participant')
    certificate_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.email
