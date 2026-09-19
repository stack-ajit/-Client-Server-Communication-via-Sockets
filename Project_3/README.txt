*-*-*-*-*-*-*-*-*-*
Name : Ajit Kumar
*-*-*-*-*-*-*-*-*-*


CSE 5344: Computer Networks 
Assignment 3: Implementation of Routing Protocol


--> Objectives 
1. To understand Routing protocols via sockets
2. To gain exposure to a practical implementation of Distance Vector Protocol
3. To simulate a router using software defined routing



--> Tools & Software 
Google Colab
Python 3.10.10



--> Packages required to run the program 
import copy
import socket
import sys
import datetime
import pytz



--> The steps to run the program 
1. Build the project and add source code files
     Keep the .config file and source_code in the same folder
2. Router  Port No
     A      5000
     B      5001
     C      5002
     D      5003
     E      5004
     F      5005
2. Open 6 terminal tabs corresponding to each router
	Run the script for each router: python3 file_name.py router_name port_no 'config_file'
	    Ex: python3 distance_vector.py "A" 5000 /Users/ajitkumar/Desktop/network.config.txt 



--> References
https://www.geeksforgeeks.org/distance-vector-routing-dvr-protocol/
https://www.youtube.com/watch?v=00AAnwgl2DI