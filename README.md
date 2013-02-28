BDII-Monitor
============

A trivial set of scripts and utilities to monitor the status of the BDII
service[1] used on grid nodes. 

Since this is based on openldap, the utilities can be reused for generic LDAP
monitoring.


Getting Started
---------------

First up, make sure that you enable the built-in monitoring that comes with
openldap >= 2.4 - see http://www.openldap.org/doc/admin24/monitoringslapd.html
for details.

To restrict access to the cn=monitor tree, you can either restrict via dn (as
shown in manpage) or via an IP address range:

  database      monitor
  access to *
    by peername.ip=128.141.0.0%255.255.0.0 read
    by peername.ip=128.142.0.0%255.255.0.0 read
    by peername.ip=137.138.0.0%255.255.0.0 read
    by * none

JSON Output
-----------

The script ldap-gather.py is based on the perl script of the same name 
but simply outputs json rather than logging to a file. This can then be
reused by other monitoring scripts


LEMON
-----

TODO - CERN Specific

collectd
--------

TODO
