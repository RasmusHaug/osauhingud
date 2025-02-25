# Generated by Django 5.1.6 on 2025-02-23 13:30

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Firma nimi peab olema 3 kuni 100 tähemärki ja koosnema tähtedest ja numbritest.', regex='^[\\w\\s\\\\p{P}]{3,100}$')])),
                ('registration_code', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Registrikood peab olema täpselt 7 numbrit.', regex='^\\d{7}$')])),
                ('date_of_establishment', models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2025, 2, 23))])),
                ('total_capital', models.PositiveIntegerField(help_text='Kogukapitali suurus eurodes (vähemalt 2500).', validators=[django.core.validators.MinValueValidator(2500)])),
            ],
        ),
        migrations.CreateModel(
            name='Shareholder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shareholder_type', models.CharField(choices=[('FÜÜSILINE', 'füüsiline isik'), ('JURIIDILINE', 'juriidiline isik')], max_length=16)),
                ('name', models.CharField(max_length=255)),
                ('registry_code_or_id', models.CharField(max_length=20)),
                ('share_size', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('shareholder_status', models.CharField(choices=[('ASUTAJA', 'asutaja'), ('ÜKS_ASUTAJATEST', 'üks asutajatests'), ('OSANIK', 'osanik')], max_length=16)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shareholders', to='companyApp.company')),
            ],
        ),
    ]
