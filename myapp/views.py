from django.shortcuts import render, HttpResponse
import json
import csv
from .models import *

# filename = "land_price_grid_2.csv"

data_list = []

# with open(filename, mode="r", newline="", encoding="utf-8") as file:
#     reader = csv.reader(file)
#     header = next(reader)  # Skip header row
    
#     for row in reader:
#         latitude = float(row[0])
#         longitude = float(row[1])
#         land_price = float(row[2])
        
#         data_list.append([latitude, longitude, land_price])
# print(data_list)

template_data = {
    "layers": [
        {"id": "renewableSources", "name": "Renewable Energy Sources", "checked": True},
        {"id": "demandCenters", "name": "Demand Centers", "checked": True},
        {"id":"landPrices", "name":"Land Price heatmap", "checked": True},
        {"id":"dottedRegion", "name":"Dotted Region", "checked": True}

    ],
    "optimisation_params": [
        {"id": "proximityRenewable", "name": "Proximity to Renewables", "value": 70},
        {"id": "marketDemand", "name": "Market Demand", "value": 80},
        {"id": "costOpt", "name": "Cost Optimisation", "value": 90}
    ],
    "map_data": {
        "renewables": [
            # {"id": 1, "type": "Solar", "name": "Bhadla Solar Park", "lat": 27.5333, "lng": 71.9167, "potential": 2245},
            # {"id": 2, "type": "Wind", "name": "Muppandal Wind Farm", "lat": 8.2718, "lng": 77.5358, "potential": 1500}
        ],
        "demand": [
            # {"id": 1, "name": "Industrial Hub - Gujarat", "lat": 23.0225, "lng": 72.5714, "demand": "High"},
            # {"id": 2, "name": "Transport Corridor - Delhi", "lat": 28.7041, "lng": 77.1025, "demand": "Medium"}
        ],
        "optimisedLocations": [
            # {"lat": 25.4358, "lng": 81.8463, "score": 95, "reason": "High solar potential, proximity to industrial demand."},
            # {"lat": 17.3850, "lng": 78.4867, "score": 88, "reason": "Balanced renewable access and emerging tech hub demand."}
        ],
        "landPrices":data_list
    },
    
}


# with open("renewable_power_plants_india_large.json", "r") as f:
#     plants = json.load(f)


# for i, plant in enumerate(plants):
#     template_data["map_data"]["renewables"].append({"id": i, **plant })

def home(request):

    # Power Plants
    plants = list(PowerPlant.objects.all().values())
    for i, plant in enumerate(plants):
        plant['lat'] = float(plant['latitude'])
        plant['lng'] = float(plant['longitude'])
        del plant['latitude']
        del plant['longitude']
        template_data["map_data"]["renewables"].append({"id": i, **plant })

    # Blocks
    blocks = list(Block.objects.all().values())
    for block in blocks:
        latitude = float(block['latitude'])
        longitude = float(block['longitude'])
        land_price = float(block['land_price'])
        score = float(block['score'])
        data_list.append([latitude, longitude, land_price, score])

    # Demand Locations
    demand_locs = list(DemandLocation.objects.all().values())
    for i, demand_loc in enumerate(demand_locs):
        demand_loc['lat'] = float(demand_loc['latitude'])
        demand_loc['lng'] = float(demand_loc['longitude'])
        del demand_loc['latitude']
        del demand_loc['longitude']
        template_data["map_data"]["demand"].append({"id": i, **demand_loc })
        

    context = {
        "template_data": template_data,
        "map_data_json": json.dumps(template_data["map_data"])
    }
    return render(request, 'myapp/home.html', context)

def block_scores(request):
    blocks = Block.objects.all()
    plants = PowerPlant.objects.all()
    demand_locs = DemandLocation.objects.all()
    for block in blocks:
        lp = block.land_price
        demand_locs_score = 0
        plants_score = 0

        for demand_loc in demand_locs:
            try:
                distance_obj = DistBtoD.objects.get(
                block_id=block.id,
                demand_location_id=demand_loc.id
                )
                demand_locs_score += (distance_obj.distance * demand_loc.weight)
            except DistBtoD.DoesNotExist:
                pass
        
        for plant in plants:
            try:
                distance_obj = DistBtoP.objects.get(
                block_id=block.id,
                power_plant_id=plant.id
                )
                plants_score += (distance_obj.distance * plant.weight)
            except DistBtoP.DoesNotExist:
                pass

        land_price_weight = 1
        block_score = demand_locs_score + plants_score + (lp*land_price_weight)
        block.score = block_score
        block.save()
    
    return HttpResponse('Block Scores Updated!')


