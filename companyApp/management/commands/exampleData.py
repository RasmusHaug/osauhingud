import json
from django.core.management.base import BaseCommand
from your_app.models import Company, Shareholder
from django.db import IntegrityError
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        json_file_path = "example_data.json"

        with open(json_file_path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)

            for row in data:
                try:
                    company_name = row["CompanyName"]
                    registration_code = row["RegistrationCode"]
                    date_of_establishment = datetime.strptime(row["DateOfEstablishment"], "%Y-%m-%d").date()
                    total_capital = row["TotalCapital"]
                    shareholders = row["Shareholders"]

                    company, created = Company.objects.get_or_create(
                        registration_code=registration_code,
                        defaults={
                            "name": company_name,
                            "date_of_establishment": date_of_establishment,
                            "total_capital": total_capital
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Company {company.name} created successfully"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Company {company.name} already exists, skipping creation"))

                    # Add shareholders
                    for shareholder in shareholders:
                        try:
                            Shareholder.objects.get_or_create(
                                company=company,
                                shareholder_type=shareholder["ShareholderType"],
                                name=shareholder["Name"],
                                registry_code_or_id=shareholder["RegistryCodeOrID"],
                                share_size=shareholder["ShareSize"],
                                shareholder_status=shareholder["ShareholderStatus"]
                            )
                            self.stdout.write(self.style.SUCCESS(f"Shareholder {shareholder['Name']} added to {company.name}"))
                        except IntegrityError as e:
                            self.stdout.write(self.style.ERROR(f"Error creating shareholder for {company.registration_code}: {str(e)}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing record {row}: {str(e)}"))

