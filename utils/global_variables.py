"""
File for global variables and settings(?)
"""
from colorama import Fore


GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
BLUE = Fore.BLUE
WHITE = Fore.WHITE
RED = Fore.RED

width = 33
line = f"{BLUE}{'-' * (width + 4)}"

port_opts = {"all": range(65535),
             "minimal": [22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443],
             "well_known": range(1023)}
