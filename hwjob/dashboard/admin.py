from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from django.views.generic.list import ListView

from dashboard.models import Client


class ClientsListView(ListView):
    """
    Returns list of clients, with optional filtering by electric heating and anomaly status.
    """
    context_object_name = "clients_list"
    template_name = "dashboard/clients_list.html"

    def get_queryset(self):
        queryset = Client.objects.all()
        elec_heating = self.request.GET.get("electric_heating")
        anomaly_status = self.request.GET.get("anomaly_status")
        if elec_heating == "yes":
            queryset = queryset.filter(has_elec_heating=True)
        elif elec_heating == "no":
            queryset = queryset.filter(has_elec_heating=False)
        if anomaly_status == "normal":
            queryset = queryset.filter(has_recent_anomaly=False)
        elif anomaly_status == "recent_anomaly":
            queryset = queryset.filter(has_recent_anomaly=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = {
            "title": "Clients list",
            "description": "Browse which clients has an electrical heating or an anomaly",
        }
        context["selected_electric_heating"] = self.request.GET.get("electric_heating", "")
        context["selected_anomaly_status"] = self.request.GET.get("anomaly_status", "")
        return context


class DashboardAdminSite(admin.sites.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path("clients", staff_member_required(ClientsListView.as_view())),
        ] + urls
        return urls
