# -*- coding: utf-8 -*-

__author__ = 'tiso'

import sys
import random
from prime_num import generate_prime, miller_rabin_test, Zpow, AlgEvklid

from socket import *

def primitve_root_mod_n(num):
    '''
    only for prime numbers
    :return: primitive root
    '''
    phi = num - 1
    n = phi
    fact = []
    i = 2
    while (i*i <= n):
        if n % i == 0:
            fact.append(i)
            while n % i == 0:
                n /= i
        i += 1

    if n > 1:
        fact.append(n)


    res = 1
    while res <= num:
        res += 1
        ok = True
        i = 0
        while i < len(fact) and ok:
            if Zpow(res, phi/fact[i], num) != 1:
                ok = False
            i += 1
        if ok:
            return res

    return None

def DiffiHellmanProtocol(host="localhost", port=10001):
    addr = (host, port)
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind((host, 10002))
    p = int(udp_socket.recvfrom(1024)[0])
    g =int( udp_socket.recvfrom(1024)[0])

    print "p: " + str(p)
    print "g: " + str(g)
    b = random.randint(10, 10**10)
    print "b: " + str(b)
    A = int(udp_socket.recvfrom(1024)[0])
    # first stage
    B = Zpow(g, b, p)   # B -> A
    udp_socket.sendto(str(B).encode(), addr)
    print "A=g**a % p = " + str(A)
    print "B=g**b % p = " + str(B)
    # second stage
    Bk = Zpow(A, b, p)    # it's B
    print "Bk=A**b % p = " + str(Bk)



def main():
    sys.stdout.write(str(DiffiHellmanProtocol()))
    return


if __name__ == "__main__":
    main()