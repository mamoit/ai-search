#!/usr/bin/python3

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from routemap import RouteMap
from client import ClientParser
import logging
import sys

from istravel_search import *

# Dictionary for the implemented algorithms
ALGORITHMS = {
    "dfs": {
        "class": ISTravelDFS,
        "label": "depth first search"
    }, "bfs": {
        "class": ISTravelBFS,
        "label": "breadth first search"
    }, "gbfs": {
        "class": ISTravelGBFS,
        "label": "greedy best first search"
    }
}


class ArgParser(ArgumentParser):
    """ Modify ArgumentParser error handling behaviour """

    def error(self, message):
        """ Writes the error message in arguments handling

        Args:
            message (str): Error message.
        """

        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    """ Main function of the program.

    Parses arguments and invokes the processing functions.
    """

    # Parse the arguments
    parser = ArgParser(description="", epilog="",
                       formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("routemap",
                        help="file where the map is defined")
    parser.add_argument("client",
                        help="file where all clients' requests are defined")

    # Mandatory to specify one and only one algorithm.
    algorithms = parser.add_mutually_exclusive_group(required=True)
    algorithms.add_argument("-dfs", action='store_true',
                            help="Use depth-first search")
    algorithms.add_argument("-bfs", action='store_true',
                            help="Use breadth-first search")
    algorithms.add_argument("-gbfs", action='store_true',
                            help="Use greedy best-first search")

    parser.add_argument("-ps", "--print-solution",
                        action="store_true",
                        help="Print solution to stdout")
    parser.add_argument("-s", "--secondary-optimization",
                        action="store_true",
                        help="Enable secondary parameter optimization")

    parser.add_argument("-p", "--plot",
                        help="plot the graph map",
                        action="store_true")
    parser.add_argument("-l", "--logfile",
                        help="file where the log is to be written to (instead \
                            of the console)")
    parser.add_argument("-v", "--verbosity",
                        help="verbosity", action="count",
                        default=0)
    parser.add_argument("-r", "--runs",
                        help="number of runs",
                        type=int,
                        default=1)
    parser.add_argument("-ns", "--no-sol",
                        help="do not write solution file (to measure algorithm \
                            performance)",
                        action="store_false")

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        filename=args.logfile,
                        level=10*(
                            (4-args.verbosity) if args.verbosity < 4 else 1
                        ))

    # parse the map file
    logging.debug("Parsing the route map file")
    route_map = RouteMap(args.routemap)
    logging.debug("Finished parsing the route map file")

    # plot the graph if needed
    if args.plot:
        logging.debug("Plotting the map graph")
        route_map.render(args.routemap)
        logging.debug("Finished plotting the map graph")

    # parse the client file
    logging.debug("Parsing the client file")
    clients = ClientParser(args.client).clients
    logging.debug("Finished parsing the client file")

    # check which algorithm to use
    if args.bfs:
        algorithm = ALGORITHMS["bfs"]
    elif args.dfs:
        algorithm = ALGORITHMS["dfs"]
    elif args.gbfs:
        algorithm = ALGORITHMS["gbfs"]
    logging.info("Using algorithm {}".format(algorithm["label"]))

    # route all the clients
    route_clients(args.client[:args.client.rfind('.')]+".sol",
                  clients,
                  route_map,
                  algorithm["class"],
                  args.secondary_optimization,
                  args.runs,
                  args.no_sol,
                  args.print_solution)


def route_clients(sol_file, clients, route_map, algorithm, sec_optim, runs, write_solution, print_solution):
    """ Routes all the clients.

    Args:
        sol_file (file): Name of the output file with all the routes.
        clients: All the Client objects.
        route_map (RouteMap): RouteMap object.
        algorithm: Class of the algorithm chosen by the user.
        sec_optim (bool): Optimize secondary weight.
        print_solution (bool): Print solution to stdout.

    """

    sol = open(sol_file, 'w') # Output file.

    logging.debug("Fulfilling clients' requests")
    for run in range(runs):
        for client in clients:
            logging.debug("Taking care of client {}".format(client))
            # Route a client and receive its path.
            path = clients[client].route(route_map, algorithm, sec_optim)
            logging.debug("{}".format(path))
            if write_solution:
                sol.write(path + "\n")
            if print_solution:
                print(path)
            logging.debug("Done with client {}".format(client))

        logging.debug("Finished fulfilling clients' requests")

if __name__ == '__main__':
    main()
