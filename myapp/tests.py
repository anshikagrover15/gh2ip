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
# from myapp.models import Block
# filename = "land_price_grid_2.csv"
# with open(filename, mode="r", newline="", encoding="utf-8") as file:
#     reader = csv.reader(file)
#     header = next(reader)  # Skip header row
    
#     for row in reader:
#         new_block = Block()
#         new_block.latitude = float(row[0])
#         new_block.longitude = float(row[1])
#         new_block.land_price = float(row[2])
#         new_block.save()
