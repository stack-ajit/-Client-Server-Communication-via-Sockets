'''
@author: Ayushi
'''

# Import libraries
import copy
import socket
import sys
import datetime
import pytz


# Get the router name and desired port number as command line arguments
router_name = sys.argv[1]
port_number = int(sys.argv[2])
file_path = sys.argv[3]


# Dictionary to get the router name from port numbers
router_port={5000: 'A', 5001: 'B', 5002: 'C', 5003: 'D', 5004: 'E', 5005: 'F'}



# n==1: Test Case 1
# n==2: Test Case 2
n=1
while n<=2:
    if n==1:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("                                          TEST CASE 1                                        ")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    if n==2:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("                                          TEST CASE 2                                        ")
        print("                                  Link Between B/D Is Broken                                 ")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        
   
    # The topology_table dictionary:
    #     Where the key is the node name and the value is a dictionary of neighbors and their associated costs.
    # The distance_vector dictionary:
    #     Where the key is the node name and the value is set to infinity (float('inf')) if the node is not the router name specified in the command line arguments, and 0 otherwise.
    # The routing_table dictionary:
    #     Where the key is the destination and the value is a tuple of (next hop, cost).

    with open(file_path) as fd:
        config_lines = fd.readlines()
        print("configuration file: ", config_lines)
        topology_table = {}
        distance_vector = {}
        routing_table = {}
        for line in config_lines:
            parts = line.strip().split("-")
            node = parts[0]
            neighbors = dict(pair.split(":") for pair in parts[1].split(","))
            topology_table[node] = neighbors
            if node != router_name:
                distance_vector[node] = "inf"
                routing_table[node] = ("", "inf")
            else:
                distance_vector[node] = 0.0
                routing_table[node] = (router_name, 0.0)
        if n==2:
            topology_table['B'].pop('D', None)
            topology_table['D'].pop('B', None)
    
        

    # Get the router's directly connected neighbors and their respective costs
    direct_neighbors = []
    for neighbor in topology_table[router_name].keys():
        direct_neighbors.append((neighbor, topology_table[router_name][neighbor]))
        # Update the distance vector for directly connected nodes
        distance_vector[neighbor]= topology_table[router_name][neighbor]
        routing_table[neighbor] = (neighbor, float(topology_table[router_name][neighbor]))



    # Print initial distance vector
    print("For Router: ", router_name)
    print("     Initial distance vector: ", distance_vector)



    # Print router IP for socket creation and binding to port number, connection type (for each router)
    ip_address = "127.0.0.1"
    connection_type = socket.SOCK_DGRAM
    print("     IP address: " + ip_address)
    print("     Port number: " + str(port_number))
    print("     Connection type: " + str(connection_type))



    # Create a UDP socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip_address, port_number))
    except Exception as e:
        print("Exception occurred: ", e)



    # Send the initial distance vector to all neighbors
    for neighbor in direct_neighbors:
        neighbor_port = 5000 + ord(neighbor[0])-ord('A')
        message = str(distance_vector)
        sock.sendto(message.encode(), (ip_address, neighbor_port))




    # Receive and handle updates from neighbors
    no_of_updates=0
    converged = False
    convergence_threshold = 10
    convergence_count = 0
    payload_size = 0
    while not converged:
        sock.settimeout(5)
        try:
            data, addr = sock.recvfrom(1024)
        except:
            convergence_count += 1
            if convergence_count > convergence_threshold:
                converged = True
                break
            else:
                continue
        
        received_vector = eval(data.decode())
        print("Received update from Router: " + router_port[addr[1]])
        print("     IP address: " + addr[0])
        print("     Message:DV(" + router_port[addr[1]] + ") --> " + str(received_vector))

        updated = False
        for node in received_vector.keys():
            new_cost = float(distance_vector[router_port[addr[1]]]) + float(received_vector[node])
            if (new_cost < float(distance_vector[node])) or (distance_vector[node] == float('inf')):
                print("     --> Previous Cost for " + node + ": " + str(distance_vector[node]))
                print("     --> Updated Cost for " + node + ": " + str(new_cost))
                distance_vector[node] = new_cost
                # Finding next hop router for destination = 'node'
                next_hop = router_port[addr[1]]
                next_hop = routing_table[next_hop][0]
                routing_table[node] = (next_hop, new_cost)
                no_of_updates += 1
                updated = True

        if updated == False:
            print("     --> No change in cost for any router")
                
        if updated:
            for neighbor in direct_neighbors:
                neighbor_port = 5000 + ord(neighbor[0])-ord('A')
                message = str(distance_vector)
                sock.sendto(message.encode(), (ip_address, neighbor_port))
                # Exclude UDP Header = 8 bytes + Ipv4 Header = 20 bytes
                payload_size = len(message.encode()) - 28

        print()



    # Print final values
    print("--------------------------------------------------------------------------")
    print("For Router: ", router_name)
    print("1) UTA ID: 1002074536")
    print("2) Total number of updates: ", no_of_updates)
    print("3) Final distance vector: ", distance_vector)
    print("4) Current date and time: ", datetime.datetime.now(pytz.utc))
    print("5) Payload size for last broadcast: ", format(payload_size) + " bytes")
    print("6) Routing table:")
    print("     {:<12} {:<11} {:<10}".format('Destination', 'Next Hop', 'Cost'))
    for node, (next_hop, cost) in routing_table.items():
        print("     {:<15} {:<9} {:<10}".format(node, next_hop, cost))

    n += 1
