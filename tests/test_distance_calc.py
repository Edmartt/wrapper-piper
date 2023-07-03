from typing import List
import pytest
from src.calculator.calc import calculate_distance

from src.calculator.models.location import Location

location_list1 = [
        Location('', 'test_location1', 5.67, 7.12),
        Location('', 'test_location2', 2.13, 76.12)
        ]


location_list2 = [
        Location('', 'test_location3', 8.12, 7.10),
        Location('', 'test_location4', 1.139, 11.14)
        ]

@pytest.mark.parametrize(
        "locations, expected",
        [(location_list1, [69.09074901895333]),
         (location_list2, [8.065727555527772])
         ]
        )
def test_calculate_distance(locations: List[Location], expected):
    assert calculate_distance(locations) == expected
