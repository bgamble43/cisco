Take static routes using CIDR notation and convert them to use subnet mask notation.
Works for NX-OS to IOS conversions

e.g. 
ip route 192.168.1.0/24 10.1.1.1 name Dummy route
converts to 
ip route 192.168.1.0 255.255.255.0 10.1.1.1 name Dummy_route
