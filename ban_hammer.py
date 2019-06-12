'''
Automatically ban peers whose sanity is either insane or unknown.
'''


import subprocess
import time
import json
import ssl

from websocket import create_connection


# Variables
SOCKET_ADDRESS = "wss://127.0.0.1:6006"  # Websocket address
BLOCK_AFTER_TIME = 1800  # Only ban peers connected longer than this
IP_TABLES_SCRIPT = "rippled_iptables.sh"  # Where to write iptables rules
WHITELIST = [] # IPs that should never be blocked


def timestamp():
    '''
    Human readable time stamp.
    '''
    return time.strftime("%y-%m-%d %H:%M:%S", time.localtime())

def websocket_command():
    '''
    Retrieve peer data from the websocket.
    '''
    socket = create_connection(
        SOCKET_ADDRESS,
        sslopt={"cert_reqs": ssl.CERT_NONE}  # Comment to enable SSL verification
    )
    socket.send(json.dumps({"command": "peers"}))
    message = socket.recv()
    socket.close()
    return message

def ip_type(address):
    '''
    Determine if address is IPv4 or IPv6 and parse accordingly.
    '''
    stamp = timestamp()

    if address[0:8] == "[::ffff:":
        address = address.split("[::ffff:")[1].split("]")[0]
        if address not in WHITELIST:
            rule = str("\niptables -I INPUT -s "
                       + address
                       + " -j DROP # Added "
                       + stamp)

    elif address[0] == "[":
        address = address.split("]:")[0]
        if address not in WHITELIST:
            rule = str("\nip6tables -I INPUT -s "
                       + address
                       + " -j DROP # Added: "
                       + stamp)

    else:
        address = address.split(":")[0]
        if address not in WHITELIST:
            rule = str("\niptables -I INPUT -s "
                       + address
                       + " -j DROP # Added: "
                       + stamp)
    return rule

def insane_peers():
    '''
    Parse `peers` response to identify insane peers IP addresses.
    '''
    rules = []
    peers = json.loads(websocket_command())['result']['peers']
    for i in peers:
        if 'sanity' in i:
            if i['sanity'] in ["insane", "unknown"] and i['uptime'] >= BLOCK_AFTER_TIME:
                rules.append(ip_type(i['address']))
    return rules

def iptables():
    '''
    Output iptables rules to a bash script & run the script.
    '''
    rules = insane_peers()
    with open(IP_TABLES_SCRIPT, 'a') as script:
        for i in rules:
            script.write(i)
    script.close()
    subprocess.call("bash " + IP_TABLES_SCRIPT, shell=True)

iptables()
