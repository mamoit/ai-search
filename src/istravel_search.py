""" Problem specific classes
"""

from uninformed_search import *
from informed_search import *
from general_search import *

from client import Client


class ISTravelSearch(GeneralSearch):
    """ Domain dependent implementation of the General Search algorithm.

    This class implements the domain-dependent methods of the general search in
    order to completelly separate the generic algorithm with the implementation
    used to solve this problem.

    Attributes:
        route_map (RouteMap): RouteMap object.
        client (Client): Client object.
        sec_optim (bool): Whether or not to optimize the second parameter in
            case there are two routes with the same cost
        route (dict): Dictionary with the nodes that compose the current route.
        open_list (list): List where the currently open nodes are stored
    """

    def __init__(self, route_map, client, sec_optim):
        """ Initialize a GeneralSearch object.

        Args:
            route_map (RouteMap): RouteMap object.
            client (Client): Client object.
            sec_optim (bool): Optimize secondary weight.
        """
        self.route_map = route_map
        self.client = client
        self.sec_optim = sec_optim

        self.route = {}
        self.open_list = []
        # Opens initial node.
        self.open_node(ISTravelNode(None, self.client.initial, None, 0, client.ti))

    def initialize(self):
        """ Initialize the node list and route.
        """
        super()
        # Opens initial node.
        self.open_node(ISTravelNode(None,
                                    self.client.initial,
                                    None,
                                    0,
                                    self.client.ti))

    def open_edge(self, node, connection):
        """ Create a new node object given a node and one of it's edges.

        Args:
            node: The node to which the connection departs from.
            connection: The given connection.

        Returns:
            The new node ready to be inserted in the route map.
        """
        adjacent = connection.get_adjacent(node.number)

        new_node = ISTravelNode(
            node,
            adjacent,
            connection,
            node.cost_so_far + connection.cost,
            connection.next_trip_time(node.time_so_far)
            + connection.duration
        )

        return new_node

    def get_valid_connections(self, node):
        """ Get a list of all the valid connections for a specific node.

        Args:
            node: The node from which the connections depart.

        Returns:
            The connections of the node which are valid giving the constraints.
        """
        return self.route_map.get_valid_connections(
            node.number,
            self.client.constraints,
            node.cost_so_far,
            node.time_so_far)

    def check_node(self, new_node):
        """ Check if a node is worth opening.

        Args:
            new_node (ISTravelNode): Node to check.

        Returns:
            True if the node is worth opening.
            False otherwise.
        """

        if new_node.number not in self.route:
            return True

        ct = self.route[new_node.number].time_so_far
        cc = self.route[new_node.number].cost_so_far

        if self.client.optimization == "tempo":
            if (self.client.goal in self.route and
                new_node.time_so_far > self.route[self.client.goal].time_so_far):
                return False
            if ct > new_node.time_so_far:
                return True
            elif (self.sec_optim and
                  ct == new_node.time_so_far and
                  cc > new_node.cost_so_far):
                return True
            return False

        elif self.client.optimization == "custo":
            if (self.client.goal in self.route and
                new_node.cost_so_far > self.route[self.client.goal].cost_so_far):
                return False
            if cc > new_node.cost_so_far:
                return True
            elif (self.sec_optim and
                  cc == new_node.cost_so_far and
                  ct > new_node.time_so_far):
                return True
            return False

    def open_node(self, new_node):
        """ Add a newly open node to the open list.

        Args:
            new_node(ISTravelNode): The node to open
        """

        self.route[new_node.number] = new_node
        if new_node.number not in self.open_list:
            self.open_list.append(new_node.number)

    def recreate(self):
        """ Recreates the path calculated.

        Given the tree calculated by the search algorithm, this function
        reconstructs the trip by backtracking from the goal node to the
        departure node.

        Returns:
            A list which represents the discovered path.
        """

        if self.client.goal not in self.route:
            return "-1"

        curr = self.route[self.client.goal]
        path = [str(self.client.goal)]
        # Lists each connection of the path
        while True:
            # check if reached top node
            if curr.parent is None:
                break
            path.append(curr.connection.transport)
            tmp = curr.parent
            path.append(str(tmp.number))
            curr = tmp

        path.reverse()

        formated_path = ""
        for node in path:
            formated_path += "{} ".format(node)

        # Appends total time and total cost at the end of the path
        formated_path += "{} {}".format(self.route[self.client.goal].time_so_far -
                                        self.client.ti,
                                        self.route[self.client.goal].cost_so_far)

        return formated_path


class ISTravelNode(Node):
    """ A node on the route tree.

    Attributes:
        parent (Node): Parent of this node.
        number (int): Number of this node.
        connection (Connection): Connection that includes this node.
        cost_so_far (int): Cost of the route so far.
        time_so_far (int): Time since the beginning of time.
    """
    def __init__(self, parent, number, connection, cost_so_far, time_so_far):
        self.parent = parent
        self.number = number
        self.connection = connection
        self.cost_so_far = cost_so_far
        self.time_so_far = time_so_far


class ISTravelBFS(BreadthFirstSearch, ISTravelSearch):
    pass


class ISTravelDFS(DepthFirstSearch, ISTravelSearch):
    pass


class ISTravelGBFS(GreedyBestFirstSearch, ISTravelSearch):
    pass
