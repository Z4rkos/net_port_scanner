#!/bin/python

from queue import Queue
import time

import utils.global_variables as g
from utils.get_args import get_args
from utils.scan_network import scan_network
from utils.port_scanner import run_port_scanner


def main() -> int:
    # Really need to reformat  the main function, way much shit here now.

    start = time.time()



    args = get_args()
    network_address = args["network"]

    print(f"{g.BLUE}[?] Scanning for hosts in the {network_address} network\n")
    
    answered = scan_network(network_address)

    if not answered:
        print(f"{g.RED}[!] No hosts found, exiting...")
        return 0

    print(f"{g.BLUE}[+] Networks:")

    print(g.line)
    print(f"IP{' ' * (g.width - 15)}MAC")
    print(g.line)

    for answer in answered:
        print(f"{g.GREEN}[+] {answer['psrc']:<{g.width-len(answer['src'])}}{answer['src']}")
    print(g.line)

    print()
    print(f"{g.BLUE}[?] Beggining port scans...")
    for answer in answered:
        ip = answer["psrc"]
        run_port_scanner(ip)
    execution_time = round(time.time() - start, 2)

    print(f"Execution time: {execution_time} seconds.")

    return 0

main()
