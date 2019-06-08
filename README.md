# rippled Ban Hammer: Ban deviant peers from rippled servers
This script uses `iptables` to block rippled peers whose `sanity` is `insane` or `unknown`. This is useful for hub operators who do not want connection slots used by peers that are not on the main net.

Specifically, the script uses a websocket request to query `rippled` for `peers`. Peers that are `insane` or whose sanity is `unknown` are appended to an external shell script (in the form of iptables rules), so they can be reviewed.

## Running the Script
This script requires the `websocket-client` package, which can be installed via pip: `pip install websocket-client`.

Modify the following variables in the `ban_hammer.py` file:
- `SOCKET_ADDRESS`: The websocket address. If you are using a `wss` (encrypted) connection and have a valid SSL/TLS certificate installed in rippled, comment the `sslopt={cert_reqs": ssl.CERT_NONE}` line in the `websocket_connection` function to enable SSL/TLS verification. The address from which you are connecting must have administrative privileges in `rippled`.
- `BLOCK_AFTER_TIME`: The time in seconds (as an integer) that a peer should be connected before it is booted. Peers that are starting can take some time to sync, so we don't want to be premature in our hammering.
- `IP_TABLES_SCRIPT`: The file to write the iptables shell script. Right now, this script will be run automatically.

After setting the variables, run the `ban_hammer.py` file.

## Limitations
- This script only works with IPv4 addresses. Eventually, it would be lovely to add IPv6 functionality.
- This script runs a shell script with the iptables rules. Using a python script to run a shell script could have security implications, particularly since iptables rules must be run as root. It is easy for a user to disable running the script, and it can be run manually instead.

## License
Anyone is free to use, modify, and distribute these scripts.

## About Me
Visit me at [https://rabbitkick.club] or on Twitter [@rabbitkickclub].


[https://rabbitkick.club]:https://rabbitkick.club
[@rabbitkickclub]:https://twitter.com/rabbitkickclub
