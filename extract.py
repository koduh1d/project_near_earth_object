import csv
import json


from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data
    about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    res = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            designation = row['pdes']
            name = row['name']
            diameter = row['diameter']
            hazardous = True if row['pha'] == 'Y' else False
            neo = NearEarthObject(
                designation=designation,
                name=name,
                diameter=diameter,
                hazardous=hazardous
            )
            res.append(neo)
    return tuple(res)


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data
    about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    res = []
    with open(cad_json_path, 'r') as f:
        contents = json.load(f)
        for d in contents['data']:
            designation = d[0]
            time = d[3]
            distance = d[4]
            velocity = d[7]
            ca = CloseApproach(
                designation=designation,
                time=time,
                distance=distance,
                velocity=velocity
            )
            res.append(ca)
    return tuple(res)
