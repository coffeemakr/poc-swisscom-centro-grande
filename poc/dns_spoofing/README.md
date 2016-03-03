# DNS Spoofing (with DHCP requests)

## Description
In order to resolve local hostnames to ip addresses the DNS server on the
centro grande writes every hostname into its own [hosts file][1].
The hostnames are provided by the DHCP requests.

An attacker may craft a DCHP request which contains a hostname like
`www.example.com`. This page will be resolved to the ip address of the
attacker. It's also possible to set spoof the address of multiple hosts by
seperating them with a space: `www.example.com example.com`

If a victim tries to visit the `www.example.com` (and doesn't use a static
DNS server) the HTTP(S) request will be directed to the attacker.  

## Proof of Concept
The script `dns_spoofing.py` is python script which will send a DHCP request
which by default spoofs the ip address of `www.example.com` and `example.com`.
After this request the script starts a minimal HTTP server as a landing page.

If the landing page is not wanted (or cherrypy is not installed)
it can be disabled by removing `start_landing_server()`.

The script has to be run with administrator / root rights e.g.:

```sh
$ sudo ./dns_spoofing.py
```

### Requirements
 * python
 * scapy
 * cherrypy (for landing page)

## Mitigation
### Client side
You are only affected if you let the DHCP client configure your the DNS server.
So using a static DNS server is an easy and save way to protect yourself:

* [List of public DNS servers](https://duckduckgo.com/?q=public+dns+server)
* [TOR DNS Resolver](https://trac.torproject.org/projects/tor/wiki/doc/DnsResolver)

### Server side
 * Escape or disallow spaces in hostnames.
 * Add a suffix to hostsnames (e.g. `.local`) or disallow dots in hostnames.

[1]: https://en.wikipedia.org/wiki/Hosts_%28file%29
