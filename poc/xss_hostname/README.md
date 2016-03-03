# XSS with Hostname

## Description

An attacker may inject malicious HTML code ([XSS][1]) by crafting a DHCP
request. The injection code is sent in the 'hostname' field of the request.
The hostname is stored temporarily on the router and is directly displayed
to the administrator in the web interface on the overview (first page after
login) and device overview page.

The attack needs some time until the data cache is updated. It also happens
in few cases that the data is perfectly escaped and displayed correctly but
this happens rarely.

It seems that the payload (hostname) is limited to ~72 characters.

## Proof of Concept

The `xss_hostname.py` script sends a DHCP request and waits for the answer.
After a run the hostname will be stored. To change the payload one can simply
edit the paramter of `send_dhcp_request(..)`.

```sh
$ sudo ./xss_hostname.py
```

### Requirements
 * python
 * [scapy](http://www.secdev.org/projects/scapy/)


[1]: https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29
