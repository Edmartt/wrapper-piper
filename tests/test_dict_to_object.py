from src.calculator.models.location import Location
from src.calculator.task import locations_dict_to_object


def test_locations_dict_to_object():

    #list of dicts with locations data
    locations_dict = [
            {'id': '', 'name': 'dict1', 'latitude': 1.234, 'longitude': 23.145}, {'id': '', 'name': 'dict2', 'latitude': 6.56, 'longitude': 3.145} 
            ]

    #list of location objects with the same data as dicts
    instances = [Location('', 'dict1', 1.234, 23.145), Location('', 'dict2', 6.56, 3.145)]

    locations_list = locations_dict_to_object(locations_dict)

    comp = [test_instance.name == real_instance.name and test_instance.latitude == real_instance.latitude and test_instance.longitude == real_instance.longitude for test_instance, real_instance in zip(instances, locations_list)]

    assert len(instances) == len(locations_list)

    assert all(comp)
