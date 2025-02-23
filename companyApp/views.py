from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.forms import formset_factory
from django.http import JsonResponse

from .models import Company, Shareholder
from .forms import CompanyForm, ShareholderForm

def index(request):
    query = request.GET.get('q', '').strip()
    companies = Company.objects.all()

    if query:
        companies = Company.objects.filter(
            Q(name__icontains=query) 
            | Q(registration_code__icontains=query)
            | Q(shareholders__name__icontains=query)
            | Q(shareholders__registry_code_or_id__icontains=query)
        ).distinct()

    return render(request, 'index.html', {'companies': companies, 'query': query})


def companyData(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    shareholders = company.shareholders.all()
    return render(request, 'company_data.html', {'company': company, 'shareholders': shareholders})

def addCompany(request):
    ShareholderFormSet = formset_factory(ShareholderForm, extra=1)
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        shareholder_form_set = ShareholderFormSet(request.POST)

        if company_form.is_valid() and shareholder_form_set.is_valid():
            company = company_form.save()

            total_share_capital = 0
            for form in shareholder_form_set:
                if form.cleaned_data.get('name'):
                    shareholder = form.save(commit=False)
                    shareholder.company = company
                    shareholder.save()
                    total_share_capital += shareholder.share_size

            if total_share_capital != company.total_capital:
                company.delete()
                error_msg = "Kogukapital peab olema võrdne osanike kapitali summaga"
                return render(request, 'company_creation.html', {
                    'company_form': company_form,
                    'shareholder_formset': shareholder_form_set,
                    'error_msg': error_msg
                })

            return redirect('company_data', company_id=company.id)

    else:
        company_form = CompanyForm()
        shareholder_form_set = ShareholderFormSet()

    return render(request, 'company_creation.html', {
        'company_form': company_form,
        'shareholder_formset': shareholder_form_set
    })

def search_shareholders(request):
    query = request.GET.get('q', '').strip()
    if query:
        shareholders = Shareholder.objects.filter(
            Q(name__icontains=query) | Q(registry_code_or_id__icontains=query)
        ).distinct('registry_code_or_id')
        companies = Company.objects.filter(
            Q(name__icontains=query) | Q(registration_code__icontains=query)
        ).distinct('registration_code')

        results = []
        for shareholder in shareholders:
            results.append({
                'name': shareholder.name,
                'registry_code_or_id': shareholder.registry_code_or_id,
                'shareholder_status': "FÜÜSILINE",
            })

        for company in companies:
            results.append({
                'name': company.name,
                'registry_code_or_id': company.registration_code,
                'shareholder_status': "JURIIDILINE",
            })

        return JsonResponse({'results': results})
    return JsonResponse({'results': []})