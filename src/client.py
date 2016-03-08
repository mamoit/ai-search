""" Client's requests
"""

from constraints import *


class ClientParser(object):
    """ Represents a client.

    Attributes:
        n (int): Number of clients.
        clients: All the clients.
    """

    def __init__(self, filename):
        """ Initialize a Client given a clients' request file

        Args:
            filename (str): Filename of the client request file.
        """

        self.parse(filename)

    def parse(self, filename):
        """ Parses the whole client request file

        Args:
            filename (str): Filename of the client request file.
        """

        with open(filename, 'r') as client_file:
            self.__parsedims(client_file)
            self.__parseclients(client_file)

    def __parsedims(self, client_file):
        """ Extracts the dimentions (number of clients) from the given file.

        Args:
            client_file (file): The file object of the clients' requests.
        """

        line = client_file.readline()
        self.n = int(line)

    def __parseclients(self, client_file):
        """ Parses each client's request from the given file.

        Args:
            client_file (file): The file object of the clients' requests.
        """

        self.clients = {}
        for line in client_file:
            new_client = Client(line)
            self.clients[new_client.number] = new_client


class Client(object):
    """ A client.

    Attributes:
        CONSTRAINT_TYPES: All the possible constraint type keys with the
            corresponding classes that handle the related constraint.
        number (int): Client number (id).
        initial (int): Initial node.
        goal (int): Goal node.
        ti (int): Starting time from which the client is available to start
            his trip.
        optimization (str): Parameter to be optimized.
        constraints: All the constraint objects that handle the requirements
            imposed by the client.
    """

    # Dictionary for constraint types.
    CONSTRAINT_TYPES = {
        "A1": ConstTransport,
        "A2": ConstConnTime,
        "A3": ConstConnCost,
        "B1": ConstTotalTime,
        "B2": ConstTotalCost,
    }

    def __init__(self, line):
        """ Initializes a Client object.

        Args:
            line (string): Line of the client file representing
                the request of one client.
        """

        line = line.replace("\n", "")
        params = line.split(' ')
        self.number = int(params[0])
        self.initial = int(params[1])
        self.goal = int(params[2])
        self.ti = int(params[3])
        self.optimization = params[4]
        self.constraints = []

        # Parse constraints.
        # params[5] is the number of constraints for this client.
        for i in range(int(params[5])):
            constraint_type = params[6+2*i]
            constraint_param = params[7+2*i]

            constraint = self.CONSTRAINT_TYPES[constraint_type](constraint_param)
            self.constraints.append(constraint)

    def route(self, route_map, algorithm, sec_optim):
        """ Routes each client.

        Args:
            route_map (RouteMap): RouteMap object containing the connections
                between cities.
            algorithm (GeneralSearch): Algorithm specified by the program user.
            sec_optim (bool): Optimize secondary weight.

        Returns:
            The string with the route information towards the solution file.
        """

        alg = algorithm(route_map,
                        self,
                        sec_optim)
        alg.calculate()

        return "{} {}".format(
            self.number,
            alg.recreate()
        )
