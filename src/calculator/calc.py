from math import sqrt
from typing import List
from .models.location import Location


def calculate_distance(locations: List[Location]) -> List[float]:

    distances = []

    for i in range(len(locations)):

        for j in range(i+1, len(locations)):

            latitude_a = locations[i].latitude
            longitude_a = locations[i].longitude
            
            latitude_b = locations[j].latitude
            longitude_b = locations[j].longitude

            distance = sqrt((latitude_a - latitude_b)**2 + (longitude_a - longitude_b)**2)
            distances.append(distance)

    return distances
