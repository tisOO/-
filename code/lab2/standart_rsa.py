# -*- coding: utf-8 -*-

from random import random
from prime_num import generate_prime, AlgEvklid, Zpow, generate_prime_fix_len, AlgEvklid_ex
import sys
import math


def generate_rsa_key(p, q, bits_len):

    n = p*q                             # modulo

    phi = (p - 1) * (q - 1)             # Euler function of n

    # let's start to generate RSA key

    pos = 256
    e = 2**int(math.sqrt(bits_len/8))
    x = 0
    y = 0
    while AlgEvklid(phi, e, x, y) != 1:
        pos <<= 1
        e = pos ** 2 + 1

    res = AlgEvklid_ex(phi, e)
    d = res['y']
    if d < 0:
        d += phi
    d %= phi


    public_key = {
        'e': e,
        'n': n
    }

    private_key = {
        'd': d,
        'n': n
    }
    return {
        'public_key': public_key,
        'private_key': private_key
    }


def generate_bad_rsa_key(p, q, e):

    n = p*q                             # modulo

    phi = (p - 1) * (q - 1)             # Euler function of n

    # let's start to generate RSA key

    pos = 256
    x = 0
    y = 0
    while AlgEvklid(phi, e, x, y) != 1:
        pos <<= 1
        e = pos ** 2 + 1

    res = AlgEvklid_ex(phi, e)
    d = res['y']
    if d < 0:
        d += phi
    d %= phi


    public_key = {
        'e': e,
        'n': n
    }

    private_key = {
        'd': d,
        'n': n
    }
    return {
        'public_key': public_key,
        'private_key': private_key
    }



def rsa_encrypt(mes, key, bits):
    length = len(mes)
    block_size = bits/2              # размер блока
    blocks = length / block_size  # 1 блок равен 1/2 ключа
    st_pos = 0
    res = ""
    f = open('out', 'wb')
    for i in xrange(blocks):

        v = ""
        f.write(str(i) + ': \n')
        for i in mes[st_pos:st_pos+block_size]:
            num = (hex(ord(i)))[2:]
            if len(num) == 1:
                num = '0' + num

            v += num
        st_pos += block_size

        v = '0x' + v
        v = long(v, 16)
        f.write(str(v) + '\n')
        cr = Zpow(v, key['public_key']['e'], key['public_key']['n'])

        wr = hex(cr)[2:-1]

        while len(wr) < bits/2:
            wr = '0' + wr

        f.write(str(wr)+'\n\n')
        res += wr
    f.close()
    return res


def rsa_decrypt(res, key, bits):
    length = len(res)
    block_size = bits/2              # размер блока
    blocks = length / block_size  # 1 блок равен 1/2 ключа
    st_pos = 0

    result = ''
    f = open('out2', 'wb')
    for i in xrange(blocks):
        v = ""
        mes = ""
        f.write(str(i)+': \n')
        for i in res[st_pos:st_pos+block_size]:
            mes += i
        st_pos += block_size
        f.write(str(mes) + '\n')
        mes = '0x' + mes
        mes = long(mes, 16)

        answer = Zpow(mes, key['private_key']['d'], key['private_key']['n'])
        f.write(str(answer)+'\n\n')
        tmp = hex(answer)[2:-1]

        if len(tmp) % 2 == 1:
            tmp = '0' + str(tmp)
        result += str(tmp.decode('hex'))

    return result