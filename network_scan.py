#!/bin/python

import socket
import threading
import time
from get_args import get_args
from colorama import Fore, init
import warnings
from cryptography import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
from scapy.all import ARPingResult
import scapy.all as scapy



# init()
GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
BLUE = Fore.BLUE
WHITE = Fore.WHITE
RED = Fore.RED


def format_answered(answered: ARPingResult) -> list[dict]:
    formated = list()
    for answer in answered:
        answer = [x for x in str(answer).split()[1:] if "=" in x]
        one = dict()

        for elem in answer:
            elem_split = elem.split("=")
            one[elem_split[0]] = elem_split[1]


        formated.append(one)

    return formated


def scan_network(network_address: str):
    answered, _ = scapy.arping(network_address,  verbose=False)
    return answered


def scan_port(host: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        state = "open"
    except TimeoutError:
        state = "closed"
    except ConnectionRefusedError:
        state = "closed"
    finally:
        color = "GREEN" if state == "open" else "GRAY"
        print(f"{eval(color)}[+] {port}: {state}")
        s.close()

def set_threads(host, ports) -> list[threading.Thread]:

    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(host, port))
        threads.append(thread)

    return threads


def main() -> int:
    # Really need to reformat  the main function, way much shit here now.

    start = time.time()

    args = get_args()

    network_address = args["network"]
    print(f"{BLUE}[?] Scanning for hosts in the {network_address} network...\n")
    
    answered = scan_network(network_address)
    formated = format_answered(answered)

    if not answered:
        print(f"{RED}[!] No hosts found, exiting...")
        return 0

    print(f"{BLUE}[+] Networks:")

    print(f"{BLUE}----------------------")
    for answer in formated:
        print(f"{GREEN}[+] {answer['psrc']}")
    print(f"{BLUE}----------------------")

    common_ports = [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443]

    print()
    print(f"{BLUE}[?] Beggining port scans...")
    for answer in formated:
        # print(answer["psrc"], answer["src"])
        host = answer["psrc"]

        print()
        print(f"{WHITE}{host}")

        threads = set_threads(host, common_ports)

        print(f"{BLUE}----------------------")
        for thread in threads:
            thread.start()

        # Wait for the last set of threads to finish
        for thread in threads:
            thread.join()
        print(f"{BLUE}----------------------")

    execution_time = round(time.time() - start, 2)

    print(f"Execution time: {execution_time} seconds.")

    return 0

main()
