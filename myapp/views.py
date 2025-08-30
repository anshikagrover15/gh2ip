from django.shortcuts import render
import json
import csv

filename = "land_price_grid_2.csv"

data_list = []

with open(filename, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header row
    
    for row in reader:
        latitude = float(row[0])
        longitude = float(row[1])
        land_price = float(row[2])
        
        data_list.append([latitude, longitude, land_price])
print(data_list)
template_data = {
    "layers": [
        {"id": "existingAssets", "name": "Existing & Planned Assets", "checked": True},
        {"id": "renewableSources", "name": "Renewable Energy Sources", "checked": True},
        {"id": "demandCenters", "name": "Demand Centers", "checked": True},
        {"id": "transportLogistics", "name": "Transport Logistics", "checked": True},
        {"id":"landPrices", "name":"Land Price heatmap", "checked": True},
        {"id":"dottedRegion", "name":"Dotted Region", "checked": True}

    ],
    "optimisation_params": [
        {"id": "proximityRenewable", "name": "Proximity to Renewables", "value": 70},
        {"id": "marketDemand", "name": "Market Demand", "value": 80},
        {"id": "costOpt", "name": "Cost Optimisation", "value": 90}
    ],
    "map_data": {

        "assets": [
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
        ],
        "landPrices":data_list
    },
    
}


with open("renewable_power_plants_india_large.json", "r") as f:
    plants = json.load(f)


for i, plant in enumerate(plants):
    template_data["map_data"]["renewables"].append({"id": i, **plant })
def home(request):
    context = {
        "template_data": template_data,
        "map_data_json": json.dumps(template_data["map_data"])
    }
    return render(request, 'myapp/home.html', context)

