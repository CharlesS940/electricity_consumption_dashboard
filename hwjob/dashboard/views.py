from django.shortcuts import render, redirect
from django.db.models import Q
from dashboard.models import Consumption, Client
from dashboard.utils import has_electric_heating, find_anomalies


def consumption_view(request, client_id):
    """
    Retrieving the last 12 months of consumption for a client for display. If the client's electric heating status or anomalies are not set, they are computed and saved.
    """
    client = Client.objects.get(id=client_id)
    queryset = Consumption.objects.filter(client__id=client_id).order_by("-year", "-month")[:12]
    consumptions = list(reversed(queryset))

    if client.has_elec_heating is None:
        client = has_electric_heating(client, consumptions, threshold=2)
        client.save()

    if any(c.has_anomaly is None for c in consumptions):
        consumptions = find_anomalies(client, consumptions)
        Consumption.objects.bulk_update(consumptions, ['has_anomaly'])
    
    context = {
        "consumptions": consumptions,
        "has_electric_heating": client.has_elec_heating,
    }
    return render(request, "dashboard/consumption_detail.html", context)

def search_client_view(request):
    """
    Search for clients by full name or client number.
    """
    query = request.GET.get("q", "").strip()
    clients = []
    if query:
        # Search by client number or by name (case-insensitive, partial match)
        clients = Client.objects.filter(
            Q(pk__iexact=query) | Q(full_name__icontains=query)
        )
        if clients.count() == 1:
            # Redirect to the detail page if exactly one match
            return redirect("dashboard:consumption_details", client_id=clients.first().pk)
    context = {
        "clients": clients,
        "query": query,
    }
    return render(request, "dashboard/search_client.html", context)
