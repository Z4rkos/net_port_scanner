# net_port_scanner
Just a little project I made for learning purposes.
It will first scan the given network or host, then do a simple port scan of the host, or all the hosts found on the network.


## Arguments:
-n/--network:
- The host or network to scan. 
- To scan an entire network, specify the network address with CIDR notation (192.168.0.0<u>/24</u>).
-p/--ports: 
- The ports to scan. 
- These are divided into modes, Nmap style:
    - "minimal" just scans the super common ports (22, 23, 25, 53, 67, 68, 80, 110, 143, 156, 443).
    - "all" scans range(65535).
    - "well_known" scnns the well known ports (range(1023)).
- Default: minimal.
-t/--threads:
- Max number of  threads to use for port scanning.
- Default: 30.
