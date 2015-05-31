# -*- coding: utf-8 -*-
import math
import sys
import time
from standart_rsa import generate_rsa_key, rsa_decrypt, rsa_encrypt, generate_bad_rsa_key

from prime_num import Zpow, generate_prime_fix_len, miller_rabin_test, AlgEvklid_ex, AlgEvklid

import gmpy2

from WienerAttack import WienerAttack
import pylab
import random

from sympy.solvers import solve
from sympy import Symbol

class BreakingRSA:

    @staticmethod
    def factorization(n, delta):
        gmpy2.get_context().precision=1000000
        t = gmpy2.mpz(gmpy2.sqrt(n))
        res = gmpy2.mpfr('0.0', 1000000)
        steps = delta-t
        print "Steps: %d" % steps

        while True:

            res = gmpy2.sqrt(t**2 - n)

            if gmpy2.is_integer(res):
                break
            if res >= n/2:
                sys.stderr.write('I can\'t solve')
                exit()

            t += 1
            steps -= 1
            if steps % 1000 == 0:
                print steps

        p = t - gmpy2.mpz(res)
        q = n/p

        return {
            'p': int(q),
            'q': int(p)
        }

    @staticmethod
    def repeat_attack(e, n, mes):
        res = Zpow(mes, e, n)
        pred = None
        while res != mes:
            pred = res
            res = Zpow(res, e, n)
        return pred

    @staticmethod
    def chines_theorem_attack(e, users_n, cr):
        m1 = users_n[1]*users_n[2]
        m2 = users_n[0]*users_n[2]
        m3 = users_n[0]*users_n[1]

        m1_inv = AlgEvklid_ex(users_n[0], m1)['y']
        m2_inv = AlgEvklid_ex(users_n[1], m2)['y']
        m3_inv = AlgEvklid_ex(users_n[2], m3)['y']

        n1 = m1_inv % users_n[0]
        n2 = m2_inv % users_n[1]
        n3 = m3_inv % users_n[2]

        S = cr[0]*n1*m1 + cr[1]*n2*m2 + cr[2]*n3*m3

        res = S % (users_n[0]*users_n[1]*users_n[2])

        res = int((res ** (1/3.0))+0.5)
        return res

    @staticmethod
    def nokey_reading(e1, e2, N, mes1, mes2):
        koef = AlgEvklid_ex(e1, e2)
        r = koef['x']
        s = koef['y']

        x = (gmpy2.powmod(mes1, r, N)*gmpy2.powmod(mes2, s, N)) % N

        return x


    @staticmethod
    def test_factorization(p, q, mes):

        print "Start test"
        bits_len = len(str(bin(p)))-2
        key = generate_rsa_key(p, q, bits_len)
        #fkey = open(infile+'key', 'w').write(key)
        print key
        res = Zpow(mes, key['public_key']['e'], key['public_key']['n'])

        print "Crypt message: %d" % res
        delta = (p*q+p*p)/2/p
        nums = BreakingRSA.factorization(key['public_key']['n'], delta)
        print "Factorization p: %s" % nums['p']
        print "Factorization q: %s" % nums['q']
        bits_len = len(str(bin(nums['p'])))-2
        rekey = generate_rsa_key(nums['p'], nums['q'], bits_len)
        print rekey
        res = Zpow(res, rekey['private_key']['d'], rekey['private_key']['n'])

        print "Decrypt message: %d" % res
        if mes != res:
            sys.stderr.write('Fatal')
            exit()
        print "End test"

    @staticmethod
    def test_repeat_attack():
        # n = 85517
        # e = 397
        # mes = 8646
        power = 16
        i = 1
        mes = 124
        xlist = []
        ylist = []
        while power < 36:
            print "Test %d:" % i
            res = None
            while res is None:
                key = WienerAttack.create_rsa_key(power)
                crypt = Zpow(mes, key['public_key']['e'], key['public_key']['n'])
                start = time.time()
                res = BreakingRSA.repeat_attack(key['public_key']['e'], key['public_key']['n'], crypt)
                finish = time.time()
            if mes != res:
                sys.stderr.write("Error. Can't decrypt message")
                exit()
            print "Key length is %s" % power
            print "Test time: %s" % (finish - start)
            xlist.append(power)
            ylist.append(finish-start)
            power += 1
            i += 1
        pylab.plot(xlist, ylist, 'r')
        pylab.show()

    @staticmethod
    def test_chines_theorem_attack():
        users_n = []
        cr = []
        mes = 456
        power = 16
        i = 0
        e = 3
        while power < 4000:
            print "Test%d" % i
            print "Key length is %d" % power
            phi = []
            for i in xrange(3):
                q = generate_prime_fix_len(power)
                while q is None:
                    q = generate_prime_fix_len(power)
                p = generate_prime_fix_len(power)
                while p is None:
                    p = generate_prime_fix_len(power)

                users_n.append(p*q)
                phi.append((p-1)*(q-1))
            pos = 8

            for i in xrange(3):
                cr.append(Zpow(mes, e, users_n[i]))
            start = time.time()
            print BreakingRSA.chines_theorem_attack(e, users_n, cr)
            finish = time.time()
            print "Test time: %s" % (finish-start)
            power *= 2
            i += 1


class RSAAttackTest:

    @staticmethod
    def test_nokey_reading():
        N = 137759
        e1 = 191
        e2 = 233
        y1 = 60197
        y2 = 63656
        print BreakingRSA.nokey_reading(e1, e2, N, y1, y2)

# if __name__ == "__main__":
    # print BreakingRSA.factorization(23360947609, 20)
    #BreakingRSA.test_repeat_attack()
    #BreakingRSA.test_chines_theorem_attack()
    #RSAAttackTest.test_nokey_reading()
    #print BreakingRSA.wienerAttack(90581, 17993)
    # power = 512
    # i = 1
    # pos = 10
    # xlist = []
    # ylist = []
    # while power < 4000:
    #     print "Test #%d" % i
    #     print "Key's length is %d" % (power*2)
    #
    #     p = None
    #     q = None
    #     while True:
    #         q = generate_prime_fix_len(power)     # generate 2nd prime
    #
    #         p = q + 10**pos
    #         while not miller_rabin_test(p, 30):
    #             p += 1
    #
    #         if q < p and q is not None and p is not None:
    #             # str_q = str(q)
    #             # str_p = str(p)
    #             # pos = 0
    #             # for j in xrange(len(str_q)+1):
    #             #     if str_q[-j] != str_p[-j]:
    #             #         pos = j
    #             # if pos != 3:
    #             #     continue
    #             break
    #
    #     print "Difference: %d" % pos
    #     print "p: %s" % p
    #     print "q: %s" % q
    #
    #     mes = p - 100
    #     print "Message: %s" % mes
    #     print "Start factorization"
    #     start = time.time()
    #     BreakingRSA.test_factorization(p, q, mes)
    #     finish = time.time()
    #     print "Test time: %s" % (finish - start)
    #     xlist.append(power)
    #     ylist.append(finish-start)
    #     power *= 2
    #
    #     i += 1
    #
    # pylab.plot(xlist, ylist, 'r')
    # pylab.show()