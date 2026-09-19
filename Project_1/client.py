'''
@author: Ayushi
'''
import socket
import sys
import time
import os

while True:
    ans = input("Do you want to access a file? (y/n): ")
    if ans == 'y':
        SERVER_ADDRESS = input("Provide server IP address: ")
        PORT = input("Provide port number: ")
        file_name = input("Provide file name: ")

        # Get file path
        fileName = os.path.abspath(file_name)

        try:
            # Create client socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the host and port to the socket
            client_socket.connect((SERVER_ADDRESS, int(PORT)))
            print('Connection established with the server {}:{}'.format(SERVER_ADDRESS, PORT))

            # Note send time
            send_time = time.time()

            # Generate client request
            request = f"GET {fileName} HTTP/1.1\r\n".encode('utf-8')

            # Send request to server 
            client_socket.send(request)

            # Store the response from server
            response=client_socket.recv(4096).decode('utf-8')

            # Note receive time
            recv_time = time.time()

            # Calculate Round Trip Time (RTT)
            RTT = (recv_time - send_time) / 1000000

            # Print server information
            print('*******************************')
            print('1. Server Hostname: ', socket.gethostbyaddr(SERVER_ADDRESS)[0])
            print('2. Client Socket Family: ', client_socket.family)
            print('3. Client Socket Type: ', client_socket.type)
            print('4. Client Socket Protocol: ', client_socket.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
            print('5. Timeout: ', client_socket.gettimeout())
            print('6. Peername: ', client_socket.getpeername())
            print('7. Round Trip Time in(ms): ', RTT)
            print('*******************************')
            print('Status message from the server response is: ', response)

        except Exception as e:
            print("An error occurred: ", e)
            # Close socket connection    
            client_socket.close()
            sys.exit(1)

        # Close socket connection    
        client_socket.close()

    else:
        print("Disconnecting from the server on your request")
        break

