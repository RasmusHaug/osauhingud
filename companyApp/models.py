from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.timezone import now

# Create your models here.

SHAREHOLDER_TYPE = [
    ("FÜÜSILINE", "Füüsiline isik"),
    ("JURIIDILINE", "Juriidiline isik")
]

SHAREHOLDER_STATUS = {
    ("ASUTAJA", "Asutaja"),
    ("ÜKS_ASUTAJATEST", "Üks asutajatests"),
    ("OSANIK", "Osanik"),
}

class Company(models.Model):
    """
    Represents a company entity.

    Attributes:
        name (str): The name of the company.
        registration_code (str): A unique registration code for the company.
        date_of_establishment (date): Date when the company was established.
        total_capital (decimal): Total capital available for the company.
    """
    name = models.CharField(
        max_length=100, 
        validators=[
            RegexValidator(
                regex=r'^[\w\s\\p{P}]{3,100}$',
                message="Firma nimi peab olema 3 kuni 100 tähemärki ning koosnema tähtedest ja numbritest"
            )
        ]
    )
    registration_code = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message="Registrikood peab olema täpselt 7 numbrit"
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
        help_text="Kogukapitali suurus eurodes (vähemalt 2500)"
    )
    
    def __str__(self):
        return f"{self.name} ({self.registration_code})"
    

class Shareholder(models.Model):
    """
    Represents a shareholder of a copmany.

    Attributes:
        company (ForeignKey): The company this shareholder belongs to.
        shareholder_type (str): The type of shareholder ('FÜÜSILINE' for individuals, 'JURIIDILINE' for companies).
        name (str): The name of the shareholder.
        registry_code_or_id (str): A unique Company registration code or Individual ID code.
        share_size (integer): Shareholder share size for the company in euros.
        shareholder_status (str): The status of the shareholder (e.g., "ASUTAJA", "ÜKS ASUTAJATEST").
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='shareholders')
    shareholder_type = models.CharField(max_length=16, choices=SHAREHOLDER_TYPE)
    name = models.CharField(max_length=255)
    registry_code_or_id = models.CharField(max_length=20)
    share_size = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    shareholder_status = models.CharField(max_length=16, choices=SHAREHOLDER_STATUS)

    def __str__(self):
        return f"{self.name} - {self.share_size} EUR"
