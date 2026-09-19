'''
@author: Ayushi
'''

import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 8080
SERVER_ADDRESS = (HOST, PORT)


# -------------- CLIENT HANDLER ----------------
def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')

    # Extract the path of the requested object from the message
    requested_file = request.splitlines()[0].split(" ")[1]

    try:
        with open(requested_file, 'rb') as file:
            # Read the content of the file
            response_data = file.read()
            response_headers = 'HTTP/1.1 200 OK\n\n'

    except (FileNotFoundError, IsADirectoryError):
        response_headers = 'HTTP/1.1 404 Not Found\n\n'
        response_data = b'<html><body><h1>404 Not Found</h1></body></html>'

    # Generate response
    response = response_headers.encode('utf-8')
    response += response_data

    # Send the content of the requested file to the connection socket
    client_socket.sendall(response)

    client_socket.close()
# -----------------------------------------------


def serve_forever():
    # Create TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to server address and server port
        server_socket.bind(SERVER_ADDRESS)

        # Set the socket to listen
        server_socket.listen(5)

        # Set a timeout of 180 seconds for the accept() function
        server_socket.settimeout(180)

        print('Server is running on {}:{}'.format(HOST, PORT))

        while True:
            try:
                # Accept connection request
                client_socket, client_address = server_socket.accept()

                # Print client information
                print('*******************************')
                print('1. Client Hostname: ', socket.gethostbyaddr(client_address[0])[0])
                print('2. Client Socket Family: ', client_socket.family)
                print('3. Client Socket Type: ', client_socket.type)
                print('4. Client Socket Protocol: ', client_socket.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY))
                print('5. Timeout: ', client_socket.gettimeout())
                print('6. Peername: ', client_socket.getpeername())
                print('*******************************')

                # Create separate thread for each connection
                client_thread = threading.Thread(target=handle_request, args=(client_socket,))
                client_thread.start()

            except socket.timeout:
                # Handle the timeout exception
                print("Timeout while waiting for a client connection")
                break
                
    except Exception as e:
        print("Exception occurred: ", e)

    finally:
        # Close the server socket and any client sockets that are still open
        server_socket.close()
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()

                
if __name__ == '__main__':
    serve_forever()
