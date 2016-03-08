""" Informed Algorithms
"""

from general_search import GeneralSearch


class GreedyBestFirstSearch(GeneralSearch):
    """ Greedy Best First Search

    Inherits from GeneralSearch class.
    """

    def select(self):
        """ Returns the opened node with the lowest cost. """
        if self.client.optimization == "custo":
            self.open_list.sort(key=lambda x: self.route[x].cost_so_far,
                                reverse=True)
        else:
            self.open_list.sort(key=lambda x: self.route[x].time_so_far,
                                reverse=True)
        return self.open_list.pop()
