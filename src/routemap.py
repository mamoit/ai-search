""" Route Map module
"""

from graphviz import Graph

from math import ceil


class RouteMap(object):
    """Represents a map of connections between cities.

    Attributes:
        dims: Dimentions of the map.
        cities: The cities.
        connections: The connections between the cities.
    """

    CITIES = 0
    CONNECTIONS = 1

    def __init__(self, filename):
        """ Initialize a RouteMap given a map file.

        Args:
            filename (str): Filename of the map file.
        """
        self.parse(filename)

    def render(self, filename):
        """ Renders the graph to a file.

        Args:
            filename (str): Filename of the map file.
        """
        dot = Graph(comment='ISTravel graph', engine='fdp')
        for city in self.cities:
            dot.node(str(city))
        ploted = []
        for node in self.connections:
            for edge in self.connections[node]:
                if edge not in ploted:
                    ploted.append(edge)
                    dot.edge(
                        str(edge.nodes[0]),
                        str(edge.nodes[1]),
                        label=edge.transport[:2]
                    )
        dot.render(filename[:filename.rfind('.')]+".gv")

    def parse(self, filename):
        """ Parses a whole map file.

        Args:
            filename (str): Filename of the map file.
        """
        with open(filename, 'r') as map_file:
            self.__parsedims(map_file)
            self.__parsecities(map_file)
            self.__parseconnections(map_file)

    def __parsedims(self, map_file):
        """ Extracts the dimentions from the given file.

        Args:
            map_file (file): The file object of the map.
        """
        line = map_file.readline().split(" ")
        self.dims = [int(x) for x in line]

    def __parsecities(self, map_file):
        """ Calculates the cities needed for the file.

        Args:
            map_file (file): The file object of the map.
        """
        self.cities = range(1, self.dims[self.CITIES]+1)

    def __parseconnections(self, map_file):
        """ Parses the connections between cities.

        Args:
            map_file (file): The file object of the map.
        """
        self.connections = {}
        for line in map_file:
            connection = Connection(line)

            nodes = connection.getNodes()
            for node in nodes:
                if not self.connections.get(node):
                    self.connections[node] = []
                self.connections[node].append(connection)

    def get_valid_connections(self, node, constraints, current_cost, duration_so_far):
        """
        """
        valid_connections = []

        if not constraints:
            valid_connections = [con for con in self.connections[node]]
        else:
            for connection in self.connections[node]:
                valid = True
                for constraint in constraints:
                    if not constraint.check_connection(connection, current_cost, duration_so_far):
                        valid = False
                        break
                if valid:
                    valid_connections.append(connection)

        return valid_connections


class Connection(object):
    """ Represents a connection between two cities.

    Attributes:
        nodes: The two nodes that are connected by this connection.
        transport (str): The mean of transportation.
        duration (int): The duration of the connection.
        cost (int): The cost of the connection.
        ti (int): Start of the first periodic trip.
        tf (int): Ending time for the periodic trips.
        period (int): Time between trips.
    """

    DAY = 1440

    def __init__(self, line):
        """ Initialize a Connection based on a set of parameters.

        Args:
            line (str): Line of the client file to be parsed.
        """
        line = line.replace("\n", "")
        params = line.split(' ')
        self.nodes = [int(x) for x in params[:2]]
        self.transport = params[2]
        self.duration = int(params[3])
        self.cost = int(params[4])
        self.ti = int(params[5])
        self.tf = int(params[6])
        self.period = int(params[7])

    def getNodes(self):
        """ Getter for the nodes which are connected by this connection.

        Returns:
            An array with the two nodes which are connected by this connection.
        """
        return self.nodes

    def get_adjacent(self, node):
        """ Gets the other endpoint of the connection.

        Args:
            node: Number of the node of departure.
        Returns:
            The destination endpoint.
        """
        if self.nodes[0] == node:
            return self.nodes[1]
        else:
            return self.nodes[0]

    def next_trip_time(self, current_time):
        """ Calculates the time of the next connection.

        Calculates the time of the next connection providing a time of the day.

        Args:
            current_time (int): Current absolute time.
        Returns:
            The time at which the next trip will occur.
        """

        td = current_time % self.DAY # time of the day
        tb = current_time - td # time previous to current day

        if td <= self.ti:
            return tb + self.ti

        tl = self.tf - (self.tf - self.ti) % self.period # time of the last transport
        if td > tl:
            return self.next_trip_time(tb + self.DAY)

        return tb + self.ti + ceil((td-self.ti)/self.period)*self.period
