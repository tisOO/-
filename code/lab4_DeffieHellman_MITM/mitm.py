# -*- coding: utf-8 -*-

from socket import *
import random
from prime_num import Zpow

def main():
    addr_server = ("localhost", 10000)
    addr_client = ("localhost", 10002)
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(("localhost", 10001))
    p = int(udp_socket.recvfrom(1024)[0])
    g = int(udp_socket.recvfrom(1024)[0])
    print p, g
    # send public variables to client
    udp_socket.sendto(str(p).encode(), addr_client)
    udp_socket.sendto(str(g).encode(), addr_client)
    my_b = random.randint(10, 10**10)
    A = int(udp_socket.recvfrom(1024)[0])
    B = Zpow(g, my_b, p)   # B -> A
    udp_socket.sendto(str(B).encode(), addr_server)
    server_key = Zpow(A, my_b, p)    # it's B
    print "Key_server: %s" % server_key

    my_A = Zpow(g, my_b, p)
    udp_socket.sendto(str(my_A).encode(), addr_client)

    my_B = int(udp_socket.recvfrom(1024)[0])
    client_key = Zpow(my_B, my_b, p)
    print "Client key: %s" % client_key

if __name__ == "__main__":
    main()