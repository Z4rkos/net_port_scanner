#!/bin/python

from queue import Queue
import time
from colorama import Fore, init

from utils.get_args import get_args
from utils.scan_network import scan_network
from utils.scan_port import port_scanner


# init()
GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
BLUE = Fore.BLUE
WHITE = Fore.WHITE
RED = Fore.RED


def main() -> int:
    # Really need to reformat  the main function, way much shit here now.

    start = time.time()

    width = 33
    line = f"{BLUE}{'-' * (width + 4)}"

    args = get_args()
    network_address = args["network"]

    print(f"{BLUE}[?] Scanning for hosts in the {network_address} network\n")
    
    answered = scan_network(network_address)

    if not answered:
        print(f"{RED}[!] No hosts found, exiting...")
        return 0

    print(f"{BLUE}[+] Networks:")

    print(line)
    print(f"IP{' ' * (width - 15)}MAC")
    print(line)
    for answer in answered:
        print(f"{GREEN}[+] {answer['psrc']:<{width-len(answer['src'])}}{answer['src']}")
    print(line)

    common_ports = [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443]

    print()
    print(f"{BLUE}[?] Beggining port scans...")
    queue = Queue()
    for answer in answered:
        # print(answer["psrc"], answer["src"])
        host = answer["psrc"]

        print()
        print(f"{WHITE}{host}")

        port_scanner(host, common_ports, 30, queue)

        while not queue.empty():
            color, port, state = queue.get()
            print(f"{eval(color)}[+] {port}: {state}")

    execution_time = round(time.time() - start, 2)

    print(f"Execution time: {execution_time} seconds.")

    return 0

main()
