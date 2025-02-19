from django.urls import path

from companyApp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("osaühingu-andmed/", views.companyData, name="company-data"),
    path("osaühingu-loomine/", views.companyCreation, name="company-creation"),
]