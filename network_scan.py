#!/bin/python

import socket
import threading
from queue import Queue
import time
from get_args import get_args
from utils.scan_network import scan_network
from colorama import Fore, init


# init()
GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
BLUE = Fore.BLUE
WHITE = Fore.WHITE
RED = Fore.RED


def scan_port(host: str, port: int, queue: Queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    state = ""
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        state = "open"
    except TimeoutError:
        state = "closed"
    except ConnectionRefusedError:
        state = "closed"
    finally:
        color = "GREEN" if state == "open" else "GRAY"

        queue.put((color, port, state))
        s.close()

def set_threads(host, ports, queue) -> list[threading.Thread]:

    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(host, port, queue))
        threads.append(thread)

    return threads


def main() -> int:
    # Really need to reformat  the main function, way much shit here now.

    start = time.time()

    args = get_args()

    network_address = args["network"]
    print(f"{BLUE}[?] Scanning for hosts in the {network_address} network...\n")
    
    answered = scan_network(network_address)

    if not answered:
        print(f"{RED}[!] No hosts found, exiting...")
        return 0

    print(f"{BLUE}[+] Networks:")

    print(f"{BLUE}----------------------")
    for answer in answered:
        print(f"{GREEN}[+] {answer['psrc']}")
    print(f"{BLUE}----------------------")

    common_ports = [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443]

    print()
    print(f"{BLUE}[?] Beggining port scans...")
    queue = Queue()
    for answer in answered:
        # print(answer["psrc"], answer["src"])
        host = answer["psrc"]

        print()
        print(f"{WHITE}{host}")

        threads = set_threads(host, common_ports, queue)

        print(f"{BLUE}----------------------")
        for thread in threads:
            thread.start()

        # Wait for the last set of threads to finish
        for thread in threads:
            thread.join()
            color, port, state = queue.get()
            print(f"{eval(color)}[+] {port} {state}")
        print(f"{BLUE}----------------------")

    
    execution_time = round(time.time() - start, 2)

    print(f"Execution time: {execution_time} seconds.")

    return 0

main()
