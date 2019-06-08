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
    socket.send(
        json.dumps(
            {
                "command": "peers",
            }
        )
    )
    message = json.loads(socket.recv())['result']['peers']
    socket.close()
    return message

def insane_peers():
    '''
    Parse `peers` response to identify insane peers IP addresses.
    This should probably also identify if IP is IPv4 or IPv6.
    '''
    bad_peers = []
    peers = websocket_command()
    for i in peers:
        if 'sanity' in i:
            if i['sanity'] in ["insane", "unknown"] and i['uptime'] >= BLOCK_AFTER_TIME:
                bad_peers.append(i['address'].split(":")[0])
    return bad_peers

def ip_rules():
    '''
    Output bad IPs to a bash script.
    '''
    bad_peers = insane_peers()
    stamp = timestamp()
    with open(IP_TABLES_SCRIPT, 'a') as script:
        for i in bad_peers:
            script.write("\niptables -I INPUT -s " + i
                         + " -m state --state NEW,ESTABLISHED,RELATED -j DROP # Added: "
                         + stamp)
    script.close()
    subprocess.call("bash " + IP_TABLES_SCRIPT, shell=True)

ip_rules()
