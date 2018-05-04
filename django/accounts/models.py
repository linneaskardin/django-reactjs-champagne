# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    name = models.CharField('Namn', max_length=255)
    phone_no = models.IntegerField('Telefonnummer', null = True) # Ta bort null = True när databasen har en superuser
    coname = models.CharField('Företagsnamn', max_length=80, default = '', null = True) # Ta bort null = True när databasen har en superuser
    reg_no = models.CharField('Organisationsnummer', max_length=13, null = True, default = 'xxxxxxxx-xxxx') # Ta bort null = True när databasen har en superuser

    def __str__(self):
        return self.email
