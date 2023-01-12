import concurrent.futures
import socket

from utils import global_variables as g


def scan_port(ip: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    state = ""
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        state = "open"
    except (TimeoutError, ConnectionRefusedError):
        state = "closed"
    finally:
        s.close()
        return state, port


def port_scanner(ip: str, ports: list[int], max_threads: int, print_closed: bool):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:

        port_futures = (executor.submit(scan_port, ip, port) for port in ports)

        for future in concurrent.futures.as_completed(port_futures):

            state, port = future.result()
            color = "GREEN" if state == "open" else "GRAY"
            color = f"g.{color}"

            if print_closed:
                print(f"{eval(color)}[+] {port}: {state}")
            elif not print_closed and state == "open":
                print(f"{eval(color)}[+] {port}: {state}")



# this is just to minimise print statements in main.
def run_port_scanner(networks: list[dict], ports: list[int], max_threads: int, print_closed: bool):
    print(f"{g.BLUE}[?] Beggining port scans...")

    for network in networks:
        ip = network["psrc"]

        print(f"{g.WHITE}[+] {ip}")
        print(g.line)
        port_scanner(ip, ports, max_threads, print_closed)
        print(g.line)

if __name__ == "__main__":
    port_scanner("10.0.0.138", [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443], 30)
