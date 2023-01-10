import warnings
from cryptography import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
from scapy.all import ARPingResult
import scapy.all as scapy


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

    answered = format_answered(answered)
    return answered
