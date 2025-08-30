from django.shortcuts import render
import json
# Create your views here.

template_data = {
    "layers": [
        {"id": "existingAssets", "name": "Existing & Planned Assets", "checked": True},
        {"id": "renewableSources", "name": "Renewable Energy Sources", "checked": True},
        {"id": "demandCenters", "name": "Demand Centers", "checked": True},
        {"id": "transportLogistics", "name": "Transport Logistics", "checked": True}
    ],
    "optimisation_params": [
        {"id": "proximityRenewable", "name": "Proximity to Renewables", "value": 70},
        {"id": "marketDemand", "name": "Market Demand", "value": 80},
        {"id": "costOpt", "name": "Cost Optimisation", "value": 90}
    ],
    "map_data": {
        "assets": [
            {"id": 1, "type": "Plant", "status": "Existing", "name": "Reliance Jamnagar Complex", "lat": 22.3733, "lng": 70.0577, "capacity": 500},
            {"id": 2, "type": "Storage", "status": "Planned", "name": "Adani Mundra Solar Park Storage", "lat": 22.84, "lng": 69.71, "capacity": 200},
            {"id": 3, "type": "Plant", "status": "Planned", "name": "ACME Solar Plant, Rajasthan", "lat": 26.9124, "lng": 75.7873, "capacity": 350}
        ],
        "renewables": [
            {"id": 1, "type": "Solar", "name": "Bhadla Solar Park", "lat": 27.5333, "lng": 71.9167, "potential": 2245},
            {"id": 2, "type": "Wind", "name": "Muppandal Wind Farm", "lat": 8.2718, "lng": 77.5358, "potential": 1500}
        ],
        "demand": [
            {"id": 1, "name": "Industrial Hub - Gujarat", "lat": 23.0225, "lng": 72.5714, "demand": "High"},
            {"id": 2, "name": "Transport Corridor - Delhi", "lat": 28.7041, "lng": 77.1025, "demand": "Medium"}
        ],
        "transport": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[70.0577, 22.3733], [72.5714, 23.0225]]}
            }]
        },
        "optimisedLocations": [
            {"lat": 25.4358, "lng": 81.8463, "score": 95, "reason": "High solar potential, proximity to industrial demand."},
            {"lat": 17.3850, "lng": 78.4867, "score": 88, "reason": "Balanced renewable access and emerging tech hub demand."}
        ]
    }
}


def home(request):
    context = {
        "template_data": template_data,
        "map_data_json": json.dumps(template_data["map_data"])
    }
    return render(request, 'myapp/home.html', context)

