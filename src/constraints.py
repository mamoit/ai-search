""" Constraints of a Client
"""


class Constraint(object):
    """ A constraint to a client's request """

    def check_connection(self, connection, current_cost, current_time):
        """ Checks if a connection is valid considering a specified criterion.

        Arguments:
            connection (Connection): connection to check.
            current_cost (int): current total route cost.
            current_time (int): current total route time.
        """

        pass


class ConstTransport(Constraint):
    """ Constraint for the type of transport not to use.

    Attributes:
        transport_type (str): Type of transport to avoid on all connections.
    """

    def __init__(self, param):
        self.transport_type = param

    def check_connection(self, connection, current_cost, current_time):
        """ Checks if the connection transport is to be avoided.

        Returns:
            True if the connection is valid.
            False otherwise.
        """

        return connection.transport != self.transport_type


class ConstConnTime(Constraint):
    """ Constraint for the time limit for each connection.

    Attributes:
        max_connection_time (int): Maximum time per connection.
    """

    def __init__(self, param):
        self.max_connection_time = int(param)

    def check_connection(self, connection, current_cost, current_time):
        """ Checks if connection time respects the user's time limit.

        Returns:
            True if the connection is valid.
            False otherwise.
        """

        return connection.duration <= self.max_connection_time


class ConstConnCost(Constraint):
    """ Constraint for the cost limit for each connection.

    Attributes:
        max_connection_cost (int): Maximum cost per connection.
    """

    def __init__(self, param):
        self.max_connection_cost = int(param)

    def check_connection(self, connection, current_cost, current_time):
        """ Checks if connection cost respects the user's cost limit.

        Returns:
            True if the connection is valid.
            False otherwise.
        """

        return connection.cost <= self.max_connection_cost


class ConstTotalTime(Constraint):
    """ Constraint for the time limit for the whole route.

    Attributes:
        max_total_time (int): Maximum time for total route.
    """

    def __init__(self, param):
        self.max_total_time = int(param)

    def check_connection(self, connection, current_cost, duration_so_far):
        """ Checks if the total route time respects the user's time limit.

        Returns:
            True if the connection is valid.
            False otherwise.
        """

        return connection.duration + duration_so_far <= self.max_total_time


class ConstTotalCost(Constraint):
    """ Constraint for the cost limit for the whole route.

    Attributes:
        max_total_cost (int): Maximum cost for total route.
    """

    def __init__(self, param):
        self.max_total_cost = int(param)

    def check_connection(self, connection, current_cost, current_time):
        """ Checks if the total route cost respects the user's cost limit.

        Returns:
            True if the connection is valid.
            False otherwise.
        """

        return connection.cost + current_cost <= self.max_total_cost
