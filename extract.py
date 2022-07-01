"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
import math

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    res = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            designation = row['pdes']
            name = row['name']
            diameter = row['diameter']
            hazardous = True if row['pha'] == 'Y' else False
            neo = NearEarthObject(designation=designation, name=name, diameter=diameter, hazardous=hazardous)
            res.append(neo)
    return tuple(res)

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    res = []
    with open(cad_json_path, 'r') as f:
        contents = json.load(f)
        for d in contents['data']:
            designation = d[0]
            time = d[3]
            distance = d[4]
            velocity = d[7]
            ca = CloseApproach(designation=designation, time=time, distance=distance, velocity=velocity)
            res.append(ca)
    return tuple(res)
