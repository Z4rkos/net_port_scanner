import concurrent.futures
import socket
from queue import Queue

from . import global_variables as g

def scan_port(host: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    state = ""
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        state = "open"
    except (TimeoutError, ConnectionRefusedError):
        state = "closed"
    finally:
        s.close()
        return state, port


def port_scanner(host: str, ports: list[int], max_threads: int, queue: Queue):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        port_futures = (executor.submit(scan_port, host, port) for port in ports)
        for future in concurrent.futures.as_completed(port_futures):

            state, port = future.result()
            color = "GREEN" if state == "open" else "GRAY"

            queue.put((color, port, state))



def run_port_scanner(ip):
    common_ports = [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443]

    queue = Queue()

    port_scanner(ip, common_ports, 30, queue)

    print()
    print(f"{g.WHITE}{ip}")
    print(g.line)
    while not queue.empty():
        color, port, state = queue.get()
        color = f"g.{color}"
        print(f"{eval(color)}[+] {port}: {state}")
    print(g.line)


if __name__ == "__main__":
    port_scanner("10.0.0.138", [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443], 30)
