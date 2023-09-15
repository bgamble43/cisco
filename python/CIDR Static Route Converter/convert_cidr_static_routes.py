from ipaddress import IPv4Network
import re
import os


if __name__ == "__main__":
    output_file = "output/routes_migrated.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Open/create file for writing migrated routes to.
    output = open(output_file, "w")

    # Open file for reading routes to be migrated
    with open("input/routes.txt", "r") as f:
        # Read each line of file into separate list item
        routes = f.read().splitlines()

for i in routes:
    # load regexp into variable
    # should match routes in the form of:
    # ip route <network/cidr> <next-hop> <name> <name string>
    # where name and name string are optional
    # e.g. ip route 192.168.1.0/24 172.16.0.1 name Dummy route
    # e.g. ip route 192.168.1.0/24 172.16.0.1
    # ip route in group 0, dest. network in group 1, dest cidr in group 2, next-hop in group 3, 
    # AD (if defined) in group 4, name in group 5, and name string in group 6
    # This will match invalid IPs, e.g. 999.999.999.999

    exp = re.compile("^(ip route\s)(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})(\/\d{1,2})\s(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})(\s\d+)*\s*(name )*(.*)$")

    # compare line from input file to regexp and load result in variable
    result = exp.findall(i)

    # print(result)

    # set ip and cidr to resultant tuple item nested in list
    ip = result[0][1]
    cidr = result[0][2]

    # combine ip and cidr into one network statement to process with IPv4Network module
    network = ip + cidr

    # process network address portion of network variable
    ip_network = IPv4Network(network).network_address

    # change cidr notation to subnet mask notation
    ip_mask = IPv4Network(network).netmask

    # concatenate results of regexp processing with IPv4Network prcessing to create new route
    # using subnet mask notation instead of cidr
    # replace space in name string with underscore
    mig_route = []
    mig_route.append(result[0][0] + str(ip_network) + " " + str(ip_mask) + " " + result[0][3] + result[0][4] +  " " + result[0][5] +  result[0][6].replace(" ","_") + "\n")
    output.writelines(mig_route)
