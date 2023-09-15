### Converts NX-OS style route protocol stanzas using CIDR notation to subnet mask notation usable on IOS

### e.g.
router eigrp 1
  network 192.168.1.0/24
!
router bgp 64512
  address-family ipv4 unicast
    network 192.168.0.0/16

### converts to 

router eigrp 1
  network 192.168.1.0 0.0.0.255 
!
router bgp 64512
  address-family ipv4 unicast
    network 192.168.0.0 mask 255.255.0.0 