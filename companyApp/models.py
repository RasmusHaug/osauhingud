from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.timezone import now

# Create your models here.

SHAREHOLDER_TYPE = [
    ("NATURAL", "füüsiline"),
    ("LEGAL", "juriidiline isik")
]

class Company(models.Model):
    name = models.CharField(
        max_length=100, 
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]{3,100}$',
                message="Firma nimi peab olema 3 kuni 100 tähemärki ja koosnema tähtedest ja numbritest."
            )
        ]
    )
    registration_code = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message="Registrikood peab olema täpselt 7 numbrit."
            )
        ]
    )
    date_of_establishment = models.DateField(
        validators=[
            MaxValueValidator(limit_value=now().date())
        ]
    )
    total_capital = models.PositiveIntegerField(
        validators=[MinValueValidator(2500)],
        help_text="Kogukapitali suurus eurodes (vähemalt 2500)."
    )
    
    def __str__(self):
        return f"{self.name} ({self.registration_code})"
    

class Shareholder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='osanik')
    shareholder_type = models.CharField(max_length=10, choices=SHAREHOLDER_TYPE)
    name = models.CharField(max_length=255)
    registry_code_or_id = models.CharField(max_length=20)
    share_size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_founder = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.share_size} EUR"
