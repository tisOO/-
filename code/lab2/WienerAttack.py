# -*- coding: utf-8 -*-

import math
import sys
import time
from standart_rsa import generate_rsa_key, rsa_decrypt, rsa_encrypt, generate_bad_rsa_key

from prime_num import Zpow, generate_prime_fix_len, miller_rabin_test, AlgEvklid_ex

import gmpy2
import random
from sympy.solvers import solve
from sympy import Symbol
import pylab

class WienerAttack:

    @staticmethod
    def create_rsa_key(size=2048):
        p = generate_prime_fix_len(size // 2)
        while p is None:
            p = generate_prime_fix_len(size // 2)
        q = generate_prime_fix_len(size // 2)
        while q is None:
            q = generate_prime_fix_len(size // 2)
        N = p * q
        phiN = (p-1)*(q-1)
        while True:
            d = random.getrandbits(size // 5)
            try:
                e = int(gmpy2.invert(d, phiN))
            except:
                continue
            if (e * d) % phiN == 1:
                break

        public_key = {
            'e': e,
            'n': N
        }

        private_key = {
            'd': d,
            'N': N
        }
        return {
            'public_key': public_key,
            'private_key': private_key
        }

    @staticmethod
    def makeNextFraction(fraction):
        (a, b) = fraction
        res = b / a
        a1 = b % a
        b1 = a
        return res, (a1, b1)

    @staticmethod
    def makeContinuedFraction(fraction):
        (a, b) = fraction
        v = []
        v.append(0)
        while not a == 1:
            r, fraction = WienerAttack.makeNextFraction(fraction)
            (a, b) = fraction
            v.append(r)
        v.append(b)
        return v

    @staticmethod
    def makeIndexedConvergent(sequence, index):
        (a, b) = (1,sequence[index])
        while index>0:
            index -= 1
            (a, b) = (b, sequence[index]*b+a)
        return (b, a)
    @staticmethod
    def makeConvergents(sequence):
        r = []
        for i in xrange(0, len(sequence)):
            r.append(WienerAttack.makeIndexedConvergent(sequence, i))
        return r

    @staticmethod
    def solveQuadratic(a, b, c):
        x = Symbol('x')
        return solve(a*x**2 + b*x + c, x)

    @staticmethod
    def wienerAttack(N, e):
        conv = WienerAttack.makeConvergents(WienerAttack.makeContinuedFraction((e, N)))
        for frac in conv:
            (k, d) = frac
            if k == 0:
                continue
            phiN = ((e*d)-1)/k
            roots = WienerAttack.solveQuadratic(1, -(N-phiN+1), N)
            if len(roots) == 2:
                p, q = roots[0] % N, roots[1] % N
                if p*q == N:
                    return p, q

if __name__ == "__main__":

    size = 32
    i = 1
    xlist = []
    ylist = []
    while size < 5000:
        print "Test: %d" % i
        print "Key's length: %d" % size
        key = WienerAttack.create_rsa_key(size)
        start = time.time()
        factorization = WienerAttack.wienerAttack(key['public_key']['n'], key['public_key']['e'])
        finish = time.time()
        print factorization
        print "Test time: %s" % (finish-start)
        xlist.append(size)
        ylist.append(finish-start)
        size *= 2
        i += 1

    pylab.plot(xlist, ylist, 'r')
    pylab.show()