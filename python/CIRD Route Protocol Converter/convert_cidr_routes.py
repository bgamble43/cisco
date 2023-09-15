from ipaddress import IPv4Network
import re
import os


if __name__ == "__main__":

    output_file = "output/route_config_migrated.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Open/create file for writing migrated routes to.
    output = open(output_file, "w")

    # Open file for reading routes to be migrated
    with open("input/route_config.txt", "r") as f:
        # Read each line of file into separate list item
        route_config = f.read().splitlines()

    proto_result = []

for i in route_config:
    # load regexp into variable
    # checks for network or aggregate-address statements

    exp = re.compile(r"^(\s*)(network|aggregate-address)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})(\/\d{1,2})(.*)$")

    # load regexp into variable
    # checks for protocol type to determine syntax when building output line
    exp_proto = re.compile(r"(router bgp|router eigrp|router ospf)")

    # compare line from input file to regexp and load result in variable
    result = exp.findall(i)
    # load proto result variable with new value if exp_proto has a result
    # otherwise take old value
    # this allows us to know which protocol stanza we're working in: eigrp
    # ospf, or bgp
    proto_result = exp_proto.findall(i) if exp_proto.findall(i) else proto_result

    # if there is a result (a match) then proceed, otherwise write that line to file
    if result:
        # set ip and cidr to resultant tuple item nested in list
        ip = result[0][2]
        cidr = result[0][3]

        # combine ip and cidr into one network statement to process with IPv4Network module
        network = ip + cidr

        # process network address portion of network variable
        ip_network = IPv4Network(network).network_address

        # change cidr notation to subnet mask notation
        ip_netmask = IPv4Network(network).netmask
        ip_hostmask = IPv4Network(network).hostmask
        

        # concatenate results of regexp processing with IPv4Network prcessing to create new line
        # using subnet mask notation instead of cidr
        mig_route = []
        # if network statement, then check for protocol type
        if result[0][1] == "network":
            # if EIGRP then no need for 'mask' string
            if proto_result[0] == "router eigrp":
                mig_route.append(result[0][0] + result[0][1] + " " + str(ip_network) + " " + str(ip_hostmask) + " " + "\n")
            # if BGP need to add 'mask' string
            elif proto_result[0] == "router bgp":
                mig_route.append(result[0][0] + result[0][1] + " " + str(ip_network) + " mask " + str(ip_netmask) + " " + "\n")
            else:
                print("Pass")
                pass
        # if not network statement and instead aggregate-address then do this stuff, adding 'summary-only' at the end
        elif result[0][1] == "aggregate-address":
            mig_route.append(result[0][0] + result[0][1] + " " + str(ip_network) + " " + str(ip_netmask) + result[0][4] + "\n")
        else:
            pass
        output.writelines(mig_route)
    else:
        mig_route = i + "\n"
        output.writelines(mig_route)
