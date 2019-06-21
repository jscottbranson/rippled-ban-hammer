# rippled Ban Hammer: Ban deviant peers from rippled servers
This script uses `iptables` to block rippled peers whose `sanity` is `insane` or `unknown`. This is useful for hub operators who do not want connection slots used by peers that are not on the main net.

Specifically, the script uses a websocket request to query `rippled` for `peers`. Peers that are `insane` or whose sanity is `unknown` are appended to an external bash script (in the form of iptables rules), so they can be reviewed. The bash script is automatically run, so iptables rules are applied.

## Running the Script
This script requires the `websocket-client` package, which can be installed via pip: `pip install websocket-client`. The script was tested using Python 3.6 & Python 3.7, and the websocket connection will likely not work as expected with Python 2.x.

Modify the following variables in the `ban_hammer.py` file:
- `SOCKET_ADDRESS`: The websocket address. If you are using a `wss` (encrypted) connection and have a valid SSL/TLS certificate installed in rippled, comment the `sslopt={cert_reqs": ssl.CERT_NONE}` line in the `websocket_connection` function to enable SSL/TLS verification. The address from which you are connecting must have administrative privileges in `rippled`.
- `BLOCK_AFTER_TIME`: The time in seconds (as an integer) that a peer should be connected before it is booted. Peers that are starting can take some time to sync, so we don't want to be premature in our hammering. 30 minutes (1800 seconds) is likely a good compromise.
- `IP_TABLES_SCRIPT`: The file to write the iptables bash script. Right now, this script will be run automatically.
- `WHITELIST`: List of IPv4 and IPv6 addresses (as strings) that should never be banned. IPv6 addresses should not be surrounded by brackets.
- `RUN_BASH_SCRIPT`: if `True`, then the iptables rules that were written will be run.

After setting the variables, run the `ban_hammer.py` file.

## Limitations
- This script runs a bash script with the iptables rules. Using a Python script to run a bash script could have security implications, particularly since iptables rules must be run as root. It is easy for a user to disable running the script, and it can be run manually instead.

## License
Anyone is free to use, modify, and distribute this script.

## About Me
Visit me at [https://rabbitkick.club] or on Twitter [@rabbitkickclub].


[https://rabbitkick.club]:https://rabbitkick.club
[@rabbitkickclub]:https://twitter.com/rabbitkickclub
