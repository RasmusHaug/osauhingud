from django.urls import path

from companyApp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("osaühing/<int:company_id>/", views.companyData, name="company_data"),
    path("osaühing/loo-uus", views.addCompany, name="company_creation"),
    path('company/<int:company_id>/add_shareholder/', views.addShareholder, name='add_shareholder'),
]