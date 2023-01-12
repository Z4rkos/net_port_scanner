from utils import global_variables as g
import warnings
from cryptography import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
from scapy.all import ARPingResult
import scapy.all as scapy


def answered_to_dicts(answered: ARPingResult) -> list[dict]:
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

    answered = answered_to_dicts(answered)
    return answered


def run_network_scanner(network_address: str):
    # All the printing makes this sooooo ugly, but not sure how else to do it.

    print(f"{g.BLUE}[?] Scanning for hosts in the {network_address} network\n")

    answered = scan_network(network_address)

    if not answered:
        print(f"{g.RED}[!] No hosts found, exiting...")
        return

    print(f"{g.BLUE}[+] Networks:")

    print(g.line)
    print(f"IP{' ' * (g.width - 15)}MAC")
    print(g.line)

    for answer in answered:
        print(f"{g.GREEN}[+] {answer['psrc']:<{g.width-len(answer['src'])}}{answer['src']}")
    print(g.line)

    return answered
