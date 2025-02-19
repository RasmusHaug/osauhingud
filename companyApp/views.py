from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def companyData(request):
    return render(request, "company-data.html")

def companyCreation(request):
    return render(request, "company-creation.html")