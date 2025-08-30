from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
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
        {"id": "landCost", "name": "Land cost", "value": 90}
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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            plantMult = int(data.get('plantMult'))
            demandMult = int(data.get('demandMult'))
            landMult = int(data.get('landMult'))
            blocks = list(BlockTable.objects.all().values())
            print(f"{plantMult}, {demandMult}, {landMult}")
            data_list = []
            top_list = [(None, None, float('inf')), (None, None, float('inf')), (None, None,float('inf'))]  # keep track of 3 top_list
            for block in blocks:

                latitude = float(block['latitude'])
                longitude = float(block['longitude'])
                score = block_scores(plantMult, demandMult,landMult, block)
                data_list.append([latitude, longitude, score])
                if score < top_list[0][2]:
                    top_list[2] = top_list[1]
                    top_list[1] = top_list[0]
                    top_list[0] = (latitude, longitude, score)
                elif score < top_list[1][2]:
                    top_list[2] = top_list[1]
                    top_list[1] = (latitude, longitude, score)
                elif score < top_list[2][2]:
                    top_list[2] = (latitude, longitude, score)
            


            return JsonResponse({'status': 'ok', 'message': data_list, 'top':top_list})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    # Power Plants
    plants = list(PowerPlant.objects.all().values())
    for i, plant in enumerate(plants):
        plant['lat'] = float(plant['latitude'])
        plant['lng'] = float(plant['longitude'])
        del plant['latitude']
        del plant['longitude']
        template_data["map_data"]["renewables"].append({"id": i, **plant })

    # Blocks
    blocks = list(BlockTable.objects.all().values())
    data_list=[]
    for block in blocks:
        latitude = float(block['latitude'])
        longitude = float(block['longitude'])
        score = block_scores(0.9,0.7,1, block)
        data_list.append([latitude, longitude, score])
        template_data["map_data"]["landPrices"].append([latitude, longitude, score])

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

def block_scores(m1, m2, m3, block):

    lp = block["land_price"]
        # demand_locs_score = 0
        # plants_score = 0

        # for demand_loc in demand_locs:
        #     try:
        #         distance_obj = DistBtoDTable.objects.get(
        #         block_id=block.id,
        #         demand_location_id=demand_loc.id
        #         )
        #         demand_locs_score += (distance_obj.distance * demand_loc.weight)
        #     except DistBtoDTable.DoesNotExist:
        #         pass
        
        # for plant in plants:
        #     try:
        #         distance_obj = DistBtoPTable.objects.get(
        #         block_id=block.id,
        #         power_plant_id=plant.id
        #         )
        #         plants_score += (distance_obj.distance * plant.weight)
        #     except DistBtoPTable.DoesNotExist:
        #         pass
    
    block_score = ((float(block["distance_demand"])*int(m2)) + (float(block["distance_plants"])*int(m1)) + (lp*int(m3)))/(m1+m2+m3)

    
    return block_score


