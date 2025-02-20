from django.urls import path

from companyApp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("osaühing/<int:company_id>/", views.companyData, name="company_data"),
    path("osaühing/loo-uus", views.companyCreation, name="company_creation"),
]