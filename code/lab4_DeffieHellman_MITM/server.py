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
    p = None
    generator = True
    udp_socket.bind((host, 10000))

    while generator:
        p = generate_prime(6007, 100)
        if p is not None:
            g = primitve_root_mod_n(p)
            if g is not None and AlgEvklid(g, p) == 1:
                generator = False

    print "p: " + str(p)
    print "g: " + str(g)
    # отправка p, q
    udp_socket.sendto(str(p).encode(), addr)
    udp_socket.sendto(str(g).encode(), addr)
    a = random.randint(10, 10**10)
    print "a: " + str(a)
    # first stage
    A = Zpow(g, a, p)   # A -> B
    udp_socket.sendto(str(A).encode(), addr)
    print "A=g**a % p = " + str(A)
    # second stage
    B = int(udp_socket.recvfrom(1024)[0])
    Ak = Zpow(B, a, p)    # it's A

    print "Ak=B**a % p = " + str(Ak)




def main():
    sys.stdout.write(str(DiffiHellmanProtocol()))
    return


if __name__ == "__main__":
    main()