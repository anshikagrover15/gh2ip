from django.db import models

# Create your models here.
class DemandLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    name = models.CharField(max_length=100, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        coords = str(self.latitude) + ',' + str(self.longitude)
        return coords
    
class PowerPlant(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    name = models.CharField(max_length=100, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        coords = str(self.latitude) + ',' + str(self.longitude)
        return coords

class Block(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    land_price = models.FloatField(default=None)
    score = models.FloatField(default=0)

    def __str__(self):
        coords = str(self.latitude) + ',' + str(self.longitude)
        return coords



class DistBtoD(models.Model):
    demand_location = models.ForeignKey(DemandLocation, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    distance = models.FloatField(help_text="Distance in kilometers")
    
    class Meta:
        unique_together = [['demand_location', 'block']]
        indexes = [
            models.Index(fields=['demand_location', 'block']),
            models.Index(fields=['distance']),
        ]

    def __str__(self):
        return str(self.distance)

class DistBtoP(models.Model):
    power_plant = models.ForeignKey(PowerPlant, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    distance = models.FloatField(help_text="Distance in kilometers")
    
    class Meta:
        unique_together = [['power_plant', 'block']]
        indexes = [
            models.Index(fields=['power_plant', 'block']),
            models.Index(fields=['distance']),
        ]

    def __str__(self):
        return str(self.distance)
    
class BlockTable(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    land_price = models.FloatField(default=None)
    score = models.FloatField(default=0)

    def __str__(self):
        coords = str(self.latitude) + ',' + str(self.longitude)
        return coords



class DistBtoDTable(models.Model):
    demand_location = models.ForeignKey(DemandLocation, on_delete=models.CASCADE)
    block = models.ForeignKey(BlockTable, on_delete=models.CASCADE)
    distance = models.FloatField(help_text="Distance in kilometers")
    
    class Meta:
        unique_together = [['demand_location', 'block']]
        indexes = [
            models.Index(fields=['demand_location', 'block']),
            models.Index(fields=['distance']),
        ]

    def __str__(self):
        return str(self.distance)

class DistBtoPTable(models.Model):
    power_plant = models.ForeignKey(PowerPlant, on_delete=models.CASCADE)
    block = models.ForeignKey(BlockTable, on_delete=models.CASCADE)
    distance = models.FloatField(help_text="Distance in kilometers")
    
    class Meta:
        unique_together = [['power_plant', 'block']]
        indexes = [
            models.Index(fields=['power_plant', 'block']),
            models.Index(fields=['distance']),
        ]

    def __str__(self):
        return str(self.distance)