from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Company

from .forms import CompanyForm 
from .forms import ShareholderForm

def index(request):
    query = request.GET.get('q', '').strip()
    companies = Company.objects.all()

    if query:
        companies = Company.objects.filter(
            Q(name__icontains=query) | Q(registration_code__icontains=query)
        ).distinct()

    return render(request, 'index.html', {'companies': companies, 'query': query})


def companyData(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    shareholders = company.shareholders.all()
    return render(request, 'company_data.html', {'company': company, 'shareholders': shareholders})

def addCompany(request):
    if request.method == 'POST':
        companyForm = CompanyForm(request.POST)

        if companyForm.is_valid():
            company = companyForm.save()
            return redirect('company_data', company_id=company.id)

    else:
        company_form = CompanyForm()

    return render(request, 'company_creation.html', {'company_form': company_form})

def addShareholder(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        shareholder_form = ShareholderForm(request.POST)
        if shareholder_form.is_valid():
            shareholder = shareholder_form.save(commit=False)
            shareholder.company = company
            shareholder.save()
            return redirect('company_data', company_id=company.id)

    else:
        shareholder_form = ShareholderForm()

    return render(request, 'add_shareholder.html', {'shareholder_form': shareholder_form, 'company': company})
