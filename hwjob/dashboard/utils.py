from dashboard.models import Consumption, Client

def has_electric_heating(client: Client, consumptions: list[Consumption], threshold=2) -> Client:
    """
    Determine if a client has electric heating based on a consumption comparison between winter and summer months.
    """
    summer_consumption = sum(c.kwh_consumed for c in consumptions if c.month in [6, 7, 8])
    winter_consumption = sum(c.kwh_consumed for c in consumptions if c.month in [12, 1, 2])
    client.has_elec_heating = winter_consumption > threshold * summer_consumption
    return client

def find_anomalies(client: Client, consumptions: list[Consumption], threshold=0.5) -> list[Consumption]:
    """
    Detect anomalies and return the updated list of consumptions.
    An anomaly is defined as a percent change greater than the threshold compared to the previous month as well as a net change higher than 200 kWh.
    In the case of electric heating customers for December and March (where we expect a rise and a drop respectively), anomalies are only flagged if the expected pattern is not followed.
    """
    consumptions[0].has_anomaly = False  # First month has no previous month to compare to
    for i in range(1, len(consumptions)):
        prev = consumptions[i-1].kwh_consumed
        curr = consumptions[i].kwh_consumed
        if client.has_elec_heating and consumptions[i].month == 12:
            consumptions[i].has_anomaly = curr < prev
        elif client.has_elec_heating and consumptions[i].month == 3:
            consumptions[i].has_anomaly = curr > prev
        else:
            change = abs(curr - prev)
            consumptions[i].has_anomaly = (change/prev > threshold) & (change > 200)
    return consumptions