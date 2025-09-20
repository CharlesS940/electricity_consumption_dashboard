from django.shortcuts import render
from dashboard.models import Consumption


def consumption_view(request, client_id):
    """
    Retrieving the last 12 months of consumption for a client
    """
    queryset = Consumption.objects.filter(client__id=client_id).order_by("-year", "-month")[:12]
    consumptions = list(reversed(queryset))
    context = {
        "consumptions": consumptions,}
    return render(request, "dashboard/consumption_detail.html", context)


def search_client_view(request):
    """
    A list of clients

    TODO client.has_elec_heating should be set
    TODO client.has_anomaly should be set
    """
    return render(request, "dashboard/search_client.html")
