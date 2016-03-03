# Version 6.14.06

## Filesystems

### Extracting

```sh
FILE=Vx226x1_61406.sig
VERSION=6.14.06
wget http://rmsdl.bluewin.ch/pirelli/${FILE}
binwalk -D squashfs:.fs ${FILE}
mv _${FILE}.extracted ${VERSION}
```


### Content


| Offset      | Name               | Content            |
| ----------- | ------------------ | ------------------ |
| 0x18 - 0x2F? | Vendor            | "swisscom"         |
| 0x06 - 0x17 | Board ID           | "96368_Swiss_S1"   |
| 0x30 - 0x36 | Version            | "6.14.0"           |
| 0x40        | Timestamp          | "2015-09-23 18:00" |
| 0x120100    | Main Squash FS     |                    |
| 0xAE0100    | Recovery Squash FS |                    |


## User Interface

| Web interface        |                                    |
| -------------------- | ---------------------------------- |
| Server               | nhttpd - Nostromo webserver        |
| Executable           | `/usr/sbin/nhttpd` (Matches the "ADB Broadband HTTP Server" header) |
| Configuration Script | `/etc/ah/UserInterface.sh`         |


### Configuration:

```
serverroot /www
serveradmin webmaster@adbglobal.com
servermimes conf/mimes
docroot /www/htdocs
docindex index.html
logpid ${PID_FILE}
user nobody
notfound 301 /ui/swc/overview/index
```

## Restricted Shell

The restricted shell (when loggin in over ssh) is [CLISH](http://clish.sourceforge.net/).
Its configuration lies in `/etc/clish`

From the docs: When the "clish" shell is launched it searches the directories held in the CLISH_PATH environment variable (or "/etc/clish:~/.clish" by default) for any files with a ".xml" extension.

A quick search says it's never set:

```sh
$ grep CLISH_PATH -r
Binary file usr/lib/libclish.so.0.0.0 matches
```

There are different views with a set of commands.

Views (`grep -i "<VIEW" -r .`):

| View | File | Access Command |
| ---- | ---- | -------------- |
| pirelli-view | main.xml | Default |
| factory-view | main.xml | `factory` |
| pirelli-config-view | config-view.xml | `configure terminal` |
| if-atm-view | if-atm-view.xml | `configure terminal` > `interface atm0` |
| if-ppp-view | if-ppp-view.xml | `configure terminal` >  `interface ppp0` |
| if-vlan-view | if-vlan-view.xml | `configure terminal` > `vlan-interface` |
| if-ptm-view | if-ptm-view.xml | `configure terminal` > `interface ptm0` |
| nas-view | nas-config.xml | `configure terminal` > `nas` |
| pirelli-if-ethernet-view | if-ethernet-view.xml |  `configure terminal` > `interface eth4` |
| pirelli-if-dot11radio-view | if-dot11radio.xml | - |
| pirelli-dhcp-config | dhcp-server.xml |  - |
| printer-view | printer-config.xml | - | |
| parental-config-view | parental-config-view.xml | - |
| group-view | group-config.xml | - |
| syslog-config-view | syslog-config-view.xml | - |
| filesharing-view | filesharing-config.xml | - |
| pirelli-if-wireless-view | if-wireless-view.xml | - |
| pirelli-qosif-view | qos-view.xml | - |
| rtsp-config-view | rtsp-config-view.xml | - |
| dns-config | dns-server.xml | - |
| igmp-config-view | igmp-config-view.xml | - |
| if-bridge-view | if-bridge-view.xml | - |
| dlna-view | dlna-config.xml | - |
| ssh-config-view | ssh-config-view.xml | - |
| captive-config-view | captive-config-view.xml | - |
| ftp-view | ftp-config.xml | - |
| pirelli-view | prod/swisscom.xml | Default in `prod/`  |
| factory-view | prod/swisscom.xml | `factory` in `prod/` |
| pirelli-anonymous-ftp-view | ftp-anonymous-config.xml | ftp-view > `anonymous` |
| alg-view | alg-view.xml | `configure termininal` > `alg` |
| user-view | user-config.xml | - |


### Hidden Commands:
**Warning: These command may brick you router! Especially `factory-mode`**

  * `factory` > `factory-mode`
  * `configure terminal` > `cmsetdsl`
  * `configure terminal` > `cmgetdsl`
  * `configure terminal` > `cli-authentication <password>`
  * `configure terminal` > `cli-authentication-stop`

Restricted by `cli-authentication` which creates `/tmp/clish-cwmp-voip`.
The password must match: `V0iPcon7ro1!` ([source](http://www.tuxone.ch/2015/01/swisscom-sip-zugangsdaten-auslesen.html))

  * `configure terminal` > `dhcp` (echo "")
  * `configure terminal` > `dhcp provider-id <provider_id>`
  * `configure terminal` > `dhcp help`

  * `configure terminal` > `cwmp help`
  * `configure terminal` > `cwmp <parameter> <value>`
  * `configure terminal` > `voip help`

  * `configure terminal` > `show cwmp`
  * `configure terminal` > `voip <profile> <parameter> <value>`
  * `configure terminal` > `show voip`



## Configuration from Swisscom

I assume all configuration files form Swisscom are stored in `/tmp` because
there are some tangling links.


```sh
find -L -type l -printf '%p -> %l\n'
```


```
./etc/voip -> /tmp/voip
./etc/passwd -> /tmp/passwd
./etc/group -> /tmp/group
./etc/samba -> /tmp/samba
./etc/resolv.conf -> /tmp/resolv.conf
./etc/dibbler/server.conf -> /tmp/dibbler/server.conf
./etc/hosts -> /tmp/hosts
./etc/TZ -> /tmp/TZ
./etc/dropbear/dropbear_dss_host_key -> /tmp/dropbear/dropbear_dss_host_key
./etc/dropbear/dropbear_rsa_host_key -> /tmp/dropbear/dropbear_rsa_host_key
./etc/fstab -> /tmp/fstab
./etc/ppp/resolv.conf -> /tmp/resolv.conf.ppp
./etc/ppp/pap-secrets -> /tmp/ppp/pap-secrets
./etc/ppp/chap-secrets -> /tmp/ppp/chap-secrets
```
