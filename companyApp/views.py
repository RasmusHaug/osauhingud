from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.db.models import Q

from .models import Company

from .forms import CompanyForm 
from .forms import ShareholderFormSet

def index(request):
    query = request.GET.get('q', '')
    companies = []
    if query:
        companies = Company.objects.filter(
            Q(name__icontains=query) | Q(registration_code__icontains=query) |
            Q(shareholders__name__icontains=query) | Q(shareholders__registry_code_or_id__icontains=query)
        ).distinct()

    return render(request, 'index.html', {'companies': companies, 'query': query})

def companyData(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    shareholders = company.shareholders.all()
    return render(request, 'company_data.html', {'company': company, 'shareholders': shareholders})

def companyCreation(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        shareholder_formset = ShareholderFormSet(request.POST)

        if company_form.is_valid() and shareholder_formset.is_valid():
            company = company_form.save()
            shareholders = shareholder_formset.save(commit=False)

            for shareholder in shareholders:
                shareholder.company = company
                shareholder.is_founder = True
                shareholder.save()

            return redirect('company_data', company_id=company.id)

    else:
        company_form = CompanyForm()
        shareholder_formset = ShareholderFormSet()

    return render(request, 'company_creation.html', {'company_form': company_form, 'shareholder_formset': shareholder_formset})