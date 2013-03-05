#!/usr/bin/python

# Trivial monitoring script to spit out LDAP server performance metrics
# based on the perl script by Matty < matty91 @ gmail dot com >
# 
# Licenced under GPL3+
# Andrew Elwell <Andrew.Elwell@cern.ch>

import ldap
import json
import argparse

# Usage: ldap-gather.py [ -s server ] [ -p port ] [ -h ] 
# Default to localhost:2170 (normal LDAP users probably want port 387)
parser = argparse.ArgumentParser(description='Gather LDAP statistics and output as json')
parser.add_argument('-s', '--server', default='localhost', help='localhost if not specified')
parser.add_argument('-p', '--port', default=2170, help='2170 if not specified')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
args = parser.parse_args()

if args.verbose:
    print("Server: %s  Port: %s\n" % (args.server, args.port))


# Stuff to gather - make tuples of DN dn and attrib to get
searchlist = {
'total_connections':('cn=Total,cn=Connections,cn=Monitor','monitorCounter'),
'bytes_sent': ('cn=Bytes,cn=Statistics,cn=Monitor','monitorCounter'),
'completed_operations': ('cn=Operations,cn=Monitor','monitorOpCompleted'),
'initiated_operations': ('cn=Operations,cn=Monitor','monitorOpInitiated'),
'referrals_sent': ('cn=Referrals,cn=Statistics,cn=Monitor','monitorCounter'),
'entries_sent': ('cn=Entries,cn=Statistics,cn=Monitor','monitorCounter'),
'bind_operations': ('cn=Bind,cn=Operations,cn=Monitor','monitorOpCompleted'),
'unbind_operations': ('cn=Unbind,cn=Operations,cn=Monitor','monitorOpCompleted'),
'add_operations': ('cn=Add,cn=Operations,cn=Monitor','monitorOpInitiated'),
'delete_operations':  ('cn=Delete,cn=Operations,cn=Monitor','monitorOpCompleted'),
'modify_operations': ('cn=Modify,cn=Operations,cn=Monitor','monitorOpCompleted'),
'compare_operations': ('cn=Compare,cn=Operations,cn=Monitor','monitorOpCompleted'),
'search_operations': ('cn=Search,cn=Operations,cn=Monitor','monitorOpCompleted'),
'write_waiters': ('cn=Write,cn=Waiters,cn=Monitor','monitorCounter'),
'read_waiters': ('cn=Read,cn=Waiters,cn=Monitor','monitorCounter'),
}

# connect to LDAP server

summary = {}

conn = ldap.initialize('ldap://%s:%s' % (args.server, args.port))
conn.simple_bind()  # async bind. use simple_bind_s() if you want sync

for key in searchlist.keys():
    b = searchlist[key][0]
    attr = searchlist[key][1]
    if args.verbose:
        print("base: %s Attrib: %s" % (b,attr))

    num = conn.search(b,ldap.SCOPE_BASE,'objectClass=*',[attr,])

    try:
        result_type, result_data = conn.result(num, 1)
        # Yes, the nested array is ugly, ugly, ugly. 
        if result_type == 101:
            val = int(result_data[0][1].values()[0][0])
	    summary[key] = val
            
    except:
        print "oops"

print json.dumps(summary)
