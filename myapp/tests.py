from django.test import TestCase

# Create your tests here.

############ Adding powerplant data ##########
# import json
# from myapp.models import PowerPlant
# with open("renewable_power_plants_india_large.json", "r") as f:
#     plants = json.load(f)

# for i in plants:
#     new_plant = PowerPlant(latitude=i['lat'], longitude=i['lng'], name=i['name'], type=i['type'], weight=0.9)
#     new_plant.save()

############ Adding Blocks ################
# import csv
# from myapp.models import BlockTable
# filename = "land_prices.csv"
# with open(filename, mode="r", newline="", encoding="utf-8") as file:
#     reader = csv.reader(file)
#     header = next(reader)  # Skip header row
    
#     for row in reader:
#         new_block = BlockTable()
#         new_block.latitude = float(row[0])
#         new_block.longitude = float(row[1])
#         new_block.land_price = float(row[2])
#         new_block.save()
# from myapp.models import BlockTable, PowerPlant, DistBtoPTable, DemandLocation, DistBtoDTable
# import math

# all_powerplants = PowerPlant.objects.all()
# all_demandsites = DemandLocation.objects.all()
# block_list = BlockTable.objects.all()

# def haversine(lat1, lon1, lat2, lon2):
#     # convert degrees to radians
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

#     # haversine formula
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1

#     a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
#     c = 2 * math.asin(math.sqrt(a))

#     # Radius of Earth in kilometers (use 3956 for miles)
#     r = 6371  
#     return c * r



# for block in block_list:
#     lat1 = block.latitude
#     lng1 = block.longitude
#     min_dist = None
#     for power_plant in all_powerplants:
#         lat2 = power_plant.latitude
#         lng2 = power_plant.longitude

#         dist = haversine(lat1, lng1, lat2, lng2)

#         if min_dist:
#             if dist < min_dist[0]:
#                 min_dist = (dist, power_plant)
#         else:
#             min_dist = (dist, power_plant)
    
   
#     for demand in all_demandsites:
#         lat2 = demand.latitude
#         lng2 = demand.longitude
#         dist = haversine(lat1, lng1, lat2, lng2)
#         sum_entry = DistBtoDTable()
#         sum_entry.block = block
#         sum_entry.demand_location = demand
#         sum_entry.distance = dist
#         sum_entry.save()


#     dist_entry = DistBtoPTable() 
#     dist_entry.block = block
#     dist_entry.power_plant = min_dist[1]
#     dist_entry.distance = min_dist[0]
#     dist_entry.save()

#     print(block)
 


from myapp.models import *

blocks = BlockTable.objects.all()
max_distance_demand = 0
max_dist_power =0 
dist_demands = []
dist_powers= []
for block in blocks:
    dist_demand =0 
    query = DistBtoDTable.objects.filter(block=block)
    for q in query:
        dist_demand += q.distance
    if dist_demand > max_distance_demand:
        max_distance_demand = dist_demand
    dist_demands.append(dist_demand)



    dist_power =0 
    query = DistBtoPTable.objects.filter(block=block)
    for q in query:
        print(block)
        dist_power += q.distance
    if dist_power > max_dist_power:
        max_dist_power = dist_power
    dist_powers.append(dist_power)

print(dist_demands[:10])
print(dist_powers[:10])

for i, block in enumerate(blocks):
    print(i)
    block.distance_demand = dist_demands[i]/max_distance_demand
    block.distance_plants = dist_powers[i]/max_dist_power
    block.save()