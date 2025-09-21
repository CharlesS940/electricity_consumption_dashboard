from django.shortcuts import render
from dashboard.models import Consumption


def consumption_view(request, client_id):
    """
    Retrieving the last 12 months of consumption for a client
    """
    queryset = Consumption.objects.filter(client__id=client_id).order_by("-year", "-month")[:12]
    consumptions = list(reversed(queryset))
    
    summer_consumption = sum(c.kwh_consumed for c in consumptions if c.month in [6, 7, 8])
    winter_consumption = sum(c.kwh_consumed for c in consumptions if c.month in [12, 1, 2])
    if winter_consumption > 2 * summer_consumption:
        electric_heating = True
    else:
        electric_heating = False
    context = {
        "consumptions": consumptions,
        "electric_heating": electric_heating
    }
    return render(request, "dashboard/consumption_detail.html", context)


def search_client_view(request):
    """
    A list of clients

    TODO client.has_elec_heating should be set
    TODO client.has_anomaly should be set
    """
    return render(request, "dashboard/search_client.html")
