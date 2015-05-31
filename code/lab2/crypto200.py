# -*- coding: utf-8 -*-

import math
import sys
import time
from standart_rsa import generate_rsa_key, rsa_decrypt, rsa_encrypt, generate_bad_rsa_key

from prime_num import Zpow, generate_prime_fix_len, miller_rabin_test, AlgEvklid_ex, AlgEvklid

from breakingrsa import BreakingRSA


def bad_koef():
    power = 2048
    pos = 311
    print "Key's length is %d" % (power*2)
    p = None
    q = None
    while True:
        q = generate_prime_fix_len(power)     # generate 2nd prime
        p = q + 10**pos
        while not miller_rabin_test(p, 30):
            p += 1

        if q < p and q is not None and p is not None:
            break

    print "Difference: %d" % pos
    print "p: %s" % p
    print "q: %s" % q

    mes = 'Access1l3v3l3S3YB@DKo3FCIENTSISNt1t'
    h = ""
    for i in mes:
        num = hex(ord(i))[2:]
        if len(num) == 1:
            num = '0' + num
        h += num
    h = '0x' + h
    mes = long(h, 16)
    print "Message: %s" % mes
    print "Start factorization"
    start = time.time()
    BreakingRSA.test_factorization(p, q, mes)
    finish = time.time()
    print "Test time: %s" % (finish - start)

def wierder():
    from WienerAttack import WienerAttack
    size = 4096
    key = WienerAttack.create_rsa_key(size)
    mes = 'LastP@ssw0rd0fth1sL3v3lPl3@s3openF1L3'
    h = ""
    for i in mes:
        num = hex(ord(i))[2:]
        if len(num) == 1:
            num = '0' + num
        h += num
    h = '0x' + h
    mes = long(h, 16)
    print key
    crypt_message = Zpow(mes, key['public_key']['e'], key['public_key']['n'])
    print crypt_message
    #print "start"
    #start = time.time()
    #factorization = WienerAttack.wienerAttack(key['public_key']['n'], key['public_key']['e'])
    finish = time.time()
    #print finish-start

if __name__ == "__main__":
    wierder()
    pass