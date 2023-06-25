import nmap
import datetime

def execute_nmap(target, arguments):
    nm = nmap.PortScanner()
    nm.scan(target, arguments=arguments)
    for host in nm.all_hosts():
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
        for protocol in nm[host].all_protocols():
            print('----------')
            print('Protocol : %s' % protocol)
    
            lport = nm[host][protocol].keys()
            lport.sort()
            for port in lport:
                print ('port : %s\tstate : %s' % (port, nm[host][protocol][port]['state']))


def ping_scan(target):
    arguments = '-R -sP'
    nm = nmap.PortScanner()
    nm.scan(target, arguments=arguments)
    result = []
    for host in nm.all_hosts():
        # date to string conversion
        nss = nm[host]
        hostname = nm[host]['hostnames'][0]['name']

        ip_address = nm[host]['addresses']['ipv4']

        try:
            mac_address = nm[host]['addresses']['mac']
            vendor = nm[host]['vendor'][mac_address]
        except KeyError:
            mac_address = 'NULL'
            vendor = 'NULL'

        state = nm[host].state()
        result.append([datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), hostname,ip_address,mac_address,vendor,state ])
    print(result)  


ping_scan('192.168.1.1/24')


