from django import forms
from django.forms import inlineformset_factory

from .models import Company
from .models import Shareholder

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'registration_code', 'date_of_establishment', 'total_capital']
        labels = {
            'name': 'Osaühingu nimi',
            'registration_code': 'Registrikood',
            'date_of_establishment': 'Asutamise Kuupäev',
            'total_capital': 'Kogukapital (€)',
        }
        error_messages = {
            'name': {
                'required': 'Osaühingu nimi peab olema täidetud.',
                'max_length': 'Osaühingu nimi ei saa olla suurem kui 100 tähemärki.',
                'min_length': 'Osaühingu nimi peab olema vähemalt 3 tähemärki.',
            },
            'registration_code': {
                'required': 'Osaühingu registrikood peab olema täiedud.',
                'invalid': 'Osaühingu registrikood on valesti sisestatud.',
            },
            'date_of_establishment': {
                'required': 'Sisesta Osaühingu asutamise kuupäev.',
                'invalid': 'Osaühingu asutamise kuupäev pole korrektses formaadis: YYYY-MM-DD',
            },
            'total_capital': {
                'required': 'Osaühingu kogukapital peab olema lisatud',
                'min_value': 'Osaühingu kogukapital peab olema vähemalt 2500€',
            },
        }

class ShareholderForm(forms.ModelForm):
    class Meta:
        model = Shareholder
        fields = ['shareholder_type', 'name', 'registry_code_or_id', 'share_size', 'is_founder']
        labels = {
            'shareholder_type': 'Osaniku tüüp',
            'name': 'Osaniku nimi',
            'registry_code_or_id': 'Registrikood või ID number',
            'share_size': 'Osaniku osa suurus (€)',
            'is_founder': 'Asutaja',
        }
        error_messages = {
            'name': {
                'required': 'Osaniku nimi peab olema täidetud.',
            },
            'registry_code_or_id': {
                'required': 'Osaniku registrikood (firma puhul) või ID number (füüsilise isiku puhul) peab olema lisatud',
            },
            'share_size': {
                'required': 'Osaniku osa suurus peab olema lisatud',
                'min_value': 'Osaniku osa suurus peab olema vähemalt 1€',
            },
        }

ShareholderFormSet = inlineformset_factory(Company, Shareholder, form=ShareholderForm, extra=1)