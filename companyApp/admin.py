from django.contrib import admin

from companyApp.models import Company, Shareholder

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_code', 'date_of_establishment', 'total_capital')
    search_fields = ('name', 'registration_code')
    list_filter = ('date_of_establishment',)

# Define a model admin class for Shareholder
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'registry_code_or_id', 'shareholder_type', 'share_size', 'company')
    search_fields = ('name', 'registry_code_or_id')
    list_filter = ('shareholder_type',)

# Register the models with their respective admin classes
admin.site.register(Company, CompanyAdmin)
admin.site.register(Shareholder, ShareholderAdmin)