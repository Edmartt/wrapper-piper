from typing import List
import pytest
from src.calculator.calc import calculate_distance

from src.calculator.models.location import Location

location_list1 = [
        Location('', 'test_location1', 5.67, 7.12),
        Location('', 'test_location2', 2.13, 76.12)
        ]


location_list2 = [
        Location('', 'test_location3', 1.23, 2.34),
        Location('', 'test_location4', 4.56, 5.67)
        ]

location_list3 = [
        Location('', 'test_location5', 3.678, -12.678),
        Location('', 'test_location6', -4.6123, 2.982)
        ]

@pytest.mark.parametrize(
        "locations, expected",
        [(location_list1, [69.09074901895333]),
         (location_list2, [4.709331162702406]),
         (location_list3, [17.719048340416027])
         ]
        )
def test_calculate_distance(locations: List[Location], expected):
    assert calculate_distance(locations) == expected
