""" General Search Algorithm
"""


class GeneralSearch(object):
    """ General search class.

    Base class for all the other search algorithms.
    The other search algorithm classes inherit from this one.

    Attributes:
        route (dict): Dictionary with the nodes that compose the current route.
        open_list (list): List where the currently open nodes are stored
    """

    def __init__(self):
        """ Placeholder for the initialization method.
        """
        pass

    def calculate(self):
        """ Run the algorithm
        """
        self.initialize()
        self.loop()

    def initialize(self):
        """ Initialize the discovered route and the open list
        """
        self.route = {}
        self.open_list = []

    def loop(self):
        """ Main algorithm loop.

        Select a node while the algorithm is not finished.
        """
        while not self.finished():
            node = self.select()

            self.expand_node(node)

    def finished(self):
        """ Tests if open_list is empty.

        Returns:
            Boolean with the result of the test.
        """

        return self.open_list == []

    def select(self):
        """ Get the next node in the open list according to the selection
            criteria.

        Returns:
            The next node.
        """
        pass

    def expand_node(self, number):
        """ Expands a node.

        Args:
            number (int): Number of the node to expand.
        """

        node = self.route[number]

        valid_connections = self.get_valid_connections(node)

        if not valid_connections:
            return

        for connection in valid_connections:
            new_node = self.open_edge(node, connection)

            if self.check_node(new_node):
                self.open_node(new_node)

    def open_edge(self, node, connection):
        """ Create a new node object given a node and one of it's edges.

        Args:
            node: The node to which the connection departs from.
            connection: The given connection.

        Returns:
            The new node ready to be inserted in the route map.
        """
        pass

    def get_valid_connections(self, node):
        """ Get a list of all the valid connections for a specific node.

        Args:
            node: The node from which the connections depart.

        Returns:
            The connections of the node which are valid.
        """
        pass

    def check_node(self, new_node):
        """ Check if a node is worth opening.

        Args:
            new_node (Node): Node to check.

        Returns:
            True if the node is worth opening.
            False otherwise.
        """
        pass

    def open_node(self, new_node):
        """ Add a newly open node to the open list.

        Args:
            new_node(Node): The node to open
        """
        pass

    def recreate(self):
        """ Recreates the path calculated.

        Given the tree calculated by the search algorithm, this function
        reconstructs the trip by backtracking from the goal node to the
        departure node.

        Returns:
            A list which represents the discovered path.
        """
        pass


class Node(object):
    """ A node on the discovered route tree
    """

    def __init__(self):
        pass
