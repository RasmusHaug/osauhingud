from django import forms
from django.forms import inlineformset_factory
from .models import Company, Shareholder

class CompanyForm(forms.ModelForm):
    """
    Form for creating and updating a Company.

    Fields:
        - name (TextInput): Name of the company.
        - registration_code (TextInput): Unique registration code.
        - date_of_establishment (DateInput): Date the company was established.
        - total_capital (NumberInput): Minimum 2500€ capital.

    Validations:
        - Name must be between 3 and 100 characters.
        - Registration code is required and must be valid.
        - Establishment date must be in the correct format (DD-MM-YYYY).
        - Capital must be at least 2500€.
    """
    class Meta:
        model = Company
        fields = ['name', 'registration_code', 'date_of_establishment', 'total_capital']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Sisesta nimi'}),
            'registration_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Osaühingu Registrikood'}),
            'date_of_establishment': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'total_capital': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Minimaalselt 2500€'}),
        }
        labels = {
            'name': 'Osaühingu nimi',
            'registration_code': 'Registrikood',
            'date_of_establishment': 'Asutamise Kuupäev',
            'total_capital': 'Kogukapital (€)',
        }
        error_messages = {
            'name': {
                'required': 'Osaühingu nimi peab olema täidetud',
                'max_length': 'Osaühingu nimi ei saa olla suurem kui 100 tähemärki',
                'min_length': 'Osaühingu nimi peab olema vähemalt 3 tähemärki',
            },
            'registration_code': {
                'required': 'Osaühingu registrikood peab olema täiedud',
                'invalid': 'Osaühingu registrikood on valesti sisestatud',
            },
            'date_of_establishment': {
                'required': 'Sisesta Osaühingu asutamise kuupäev',
                'invalid': 'Osaühingu asutamise kuupäev pole korrektses formaadis: DD-MM-YYYY',
            },
            'total_capital': {
                'required': 'Osaühingu kogukapital peab olema lisatud',
                'min_value': 'Osaühingu kogukapital peab olema vähemalt 2500€',
            },
        }

class ShareholderForm(forms.ModelForm):
    """
    Form for adding shareholders to a company.

    Fields:
        - shareholder_type (Select): Determines if the shareholder is an individual or a company.
        - name (TextInput): The name of the shareholder.
        - registry_code_or_id (TextInput): The personal ID or company registration number.
        - share_size (NumberInput): The shareholder's financial contribution.
        - shareholder_status (Select): The status of the shareholder (e.g., "ASUTAJA", "ÜKS ASUTAJATEST").

    Behavior:
        - The first shareholder is set to "ASUTAJA" by default.
        - Subsequent shareholders are labeled as "ÜKS ASUTAJATEST".
    """
    class Meta:
        model = Shareholder
        fields = ['shareholder_type', 'name', 'registry_code_or_id', 'share_size', 'shareholder_status']
        widgets = {
            'shareholder_type': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Osaniku nimi'}),
            'registry_code_or_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Registri- või isikukood'}),
            'share_size': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Osaniku osa suurus (€)'}),
            'shareholder_status': forms.Select(attrs={'class': 'form-input'}),
        }
        labels = {
            'shareholder_type': 'Osaniku tüüp',
            'name': 'Osaniku nimi',
            'registry_code_or_id': 'Registrikood või isikukood',
            'share_size': 'Osaniku osa suurus (€)',
            'shareholder_status': 'Osaniku staatus',
        }
        error_messages = {
            'name': {
                'required': 'Osaniku nimi peab olema täidetud',
            },
            'registry_code_or_id': {
                'required': 'Osaniku registrikood (firma puhul) või ID number (füüsilise isiku puhul) peab olema lisatud',
            },
            'share_size': {
                'required': 'Osaniku osa suurus peab olema lisatud',
                'min_value': 'Osaniku osa suurus peab olema vähemalt 1€',
            },
        }

ShareholderFormSet = inlineformset_factory(Company, Shareholder, form=ShareholderForm, extra=1, can_delete=False)
