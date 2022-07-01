import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly,
    each output row
    corresponds to the information in a single close approach
    from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the
    data should be saved.
    """
    fieldnames = (
        'datetime_utc',
        'distance_au',
        'velocity_km_s',
        'designation',
        'name',
        'diameter_km',
        'potentially_hazardous'
    )
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for r in results:
            datetime = r.time
            distance = r.distance
            velocity = r.velocity
            designation = r.designation
            name = '' if r.neo.name in ('', None)\
                else r.neo.name
            diameter = '' if r.neo.diameter in ('', 'nan')\
                else r.neo.diameter
            hazardous = True if r.neo.hazardous in (1, 'Y', 'True', True)\
                else False
            row = [
                datetime,
                distance,
                velocity,
                designation,
                name,
                diameter,
                hazardous
            ]
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`.
    Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the
    data should be saved.
    """
    with open(filename, 'w') as f:
        res = [r.serialize() for r in results]
        json.dump(res, f)
