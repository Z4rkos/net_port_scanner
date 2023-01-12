#!/bin/python

import time

import utils.global_variables as g
from utils.get_args import get_args
from modules.network_scanner import run_network_scanner
from modules.port_scanner import run_port_scanner


def main():

    start = time.time()

    args = get_args()
    network_address = args["network"]
    ports = g.port_opts[args["ports"]]
    max_threads = args["threads"]

    networks = run_network_scanner(network_address)

    print_closed = True if args["ports"] == "minimal" else False

    run_port_scanner(networks, ports, max_threads, print_closed)

    execution_time = round(time.time() - start, 2)
    print(f"Execution time: {execution_time} seconds.")



if __name__ == "__main__":
    main()
