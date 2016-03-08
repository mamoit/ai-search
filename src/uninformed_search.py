""" Uninformed Algorithms
"""

from general_search import GeneralSearch


class DepthFirstSearch(GeneralSearch):
    """ Depth First Search

    Inherits from GeneralSearch class.
    """

    def select(self):
        """ Returns the last opened node. """

        return self.open_list.pop()

class BreadthFirstSearch(GeneralSearch):
    """ Breadth First Search

    Inherits from GeneralSearch class.
    """

    def select(self):
        """ Returns the first opened node. """
        return self.open_list.pop(0)
