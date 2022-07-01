import math


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections
        of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches
        to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close
        approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self.neos_by_designation = {}
        for n in neos:
            self.neos_by_designation[n.designation] = n
        self.neos_by_name = {}
        for n in neos:
            self.neos_by_name[n.name] = n
        self.approaches = {}
        for a in approaches:
            if a.designation not in self.approaches:
                self.approaches[a.designation] = [a]
            else:
                self.approaches[a.designation].append(a)
        for n in self.neos_by_designation.values():
            if n.designation in self.approaches:
                n.approaches = self.approaches[n.designation]
                for a in self.approaches[n.designation]:
                    a.neo = n

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary
        designation, or `None`.
        """
        # TODO: Fetch an NEO by its primary designation.
        if designation not in self.neos_by_designation:
            return None
        return self.neos_by_designation[designation]

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # TODO: Fetch an NEO by its name.
        if name not in self.neos_by_name:
            return None
        return self.neos_by_name[name]

    def query(self, filters=()):
        """Query close approaches to generate those that match a
        collection of filters.

        This generates a stream of `CloseApproach` objects
        that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in
        internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing
        user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for ls in self.approaches.values():
            for a in ls:
                invalid = False
                if len(filters) != 0:
                    for k, v in filters.items():
                        if k == 'date' and a.time.date() != v:
                            invalid = True
                        if k == 'start_date' and a.time.date() < v:
                            invalid = True
                        if k == 'end_date' and a.time.date() > v:
                            invalid = True
                        if k == 'distance_min' and a.distance < v:
                            invalid = True
                        if k == 'distance_max' and a.distance > v:
                            invalid = True
                        if k == 'velocity_min' and a.velocity < v:
                            invalid = True
                        if k == 'velocity_max' and a.velocity > v:
                            invalid = True
                        if k in ('diameter_min', 'diameter_max') and \
                                math.isnan(a.neo.diameter):
                            invalid = True
                        if k == 'diameter_min' and a.neo.diameter < v:
                            invalid = True
                        if k == 'diameter_max' and a.neo.diameter > v:
                            invalid = True
                        if k == 'hazardous' and a.neo.hazardous != v:
                            invalid = True
                        if invalid:
                            break
                if not invalid:
                    yield a
