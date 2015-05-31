# -*- coding: utf-8 -*-

import random                   # библиотека для работы со случайными числами
import sys
import timeit

'''
Генерация простого числа
произвольной длины.
'''

def Zpow(a, p, m):
    """
    Функция возведения в степень по модулю
    принимает 3 аргумента
    a - сам математический аргумент, возводимое число
    p - степень
    m - модуль
    """
    result = 1
    while p > 2: # когда степень сократится до квадрата и меньше - завершаем
        if p % 2 == 0: # если степень кратна 2
            a = (a ** 2) % m
            p = p // 2 # целочисленное деление (на всякий)
        else:
            result = (result * a) % m
            p = p - 1
    a = (a ** p) % m
    result = (result * a) % m
    return result

def miller_rabin_test(m, r):
    '''
    Вероятностый полинимиальный тест простоты
    :param x: входное число
    :param r: число раундов проверки на простоту, чем больше раундов, тем лучше проверка
    :return: возвращает или False - составное, или True - вероятно простое
    '''
    if m < 4:                   # 1 - не простое число
        return False
    if m == 3:
        return True             #
    if m % 2 == 0:
        return False            # число составное, так как делится на 2

    # условия выше можно убрать, так как в тест Миллера-Рабина должны даваться
    # числа большие 3 и нечетные. Если эти условия будут проверяться до вызова
    # функции, то будет теряться только время. Я оставляю эти условия
    # для защиты от дурака

    # Представим  m - 1 = 2^s*t, найдем t - нечетное.

    buf_m = m - 1
    s = 0

    while buf_m % 2 == 0:
        buf_m /= 2
        s += 1

    t = buf_m

    for i in range(0, r):       # первый цикл
        a = random.randint(2, m - 2)
        #x = a**t % m            # можно при помощи алгоритма возведения в степень по модулю
        x = Zpow(a, t, m)        # это алгоритм не самый оптимальный, лучше Монтгомери, но я пока не осилил,
                                 # у меня есть исходник свой, который я давно писал, но я его не совсем понял :D
        if x == 1 or x == m - 1:
            continue            # перейти на следующую итерацию
        trigger = False         # служебный
        for j in range(0, s-1):
            x = x**2 % m
            if x == 1:
                return False
            if x == m - 1:
                trigger = True
        if trigger:
            continue
        return False
    return True                 # вероятно простое


def AlgEvklid(a, b, d=0, x=0, y=0):
    '''
    Расширенный алгоритм Евклида
    :param a:
    :param b:
    :param d: НОД
    :param x:
    :param y:
    :return: НОД
    '''
    if ( b == 0 ):
              d = a
              x = 1
              y = 0
              return y
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while (b > 0):
              q = a / b
              r = a - q*b
              x = x2 -q*x1
              y = y2 -q*y1
              a = b
              b = r
              x2 = x1
              x1 = x
              x1 =x
              y2 = y1
              y1 = y
    d = a
    x = x2
    y = y2
    return d


def AlgEvklid_ex(a, b, d=0, x=0, y=0):
    '''
    Расширенный алгоритм Евклида
    :param a:
    :param b:
    :param d: НОД
    :param x:
    :param y:
    :return: НОД
    '''
    if ( b == 0 ):
              d = a
              x = 1
              y = 0
              return y
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while (b > 0):
              q = a / b
              r = a - q*b
              x = x2 -q*x1
              y = y2 -q*y1
              a = b
              b = r
              x2 = x1
              x1 = x
              x1 =x
              y2 = y1
              y1 = y
    d = a
    x = x2
    y = y2
    return {
        'gcd': d,
        'x': x,
        'y': y
    }


def generate_prime(S, max_count = 100):
    '''
    Генерация простого числа
    :param S: простое число
    :param max_count: максимальное число итераций на поиск простого числа
    :return: существенно большее простое число или None, если такое не найдено
    '''
    step = 0
    while True:
        R = random.randint(2, 4*S+2)
        if R % 2 != 0:
            R += 1
        N = S*R + 1
        # проверка на отсутствие малых простых делителей,
        # этот пункт опускаю, так как осуществляю проверку в Рабине-Миллере

        # проверка Миллер-Рабин
        if miller_rabin_test(N, 50):
            for i in range(1000):
                a = random.randint(2, N-1)
                if Zpow(a, N-1, N) == 1:
                    return N
        step += 1
        if step > max_count:
            return None
    return


def generate_prime_fix_len(bits_len):
    '''
    :param bits_len: битовая длина выходного числа
    :return: prime number
    '''
    if bits_len < 1:
        return False
    border1 = 2**(bits_len-1)
    border2 = 2**bits_len-1
    primes = []
    fin = open('prime20k', 'r')
    for num in fin:
        primes.append(int(num))

    while True:
        is_prime = True
        num = random.randint(border1, border2)
        if num % 2 == 0:
            continue
        for divider in primes:
            if num % divider == 0:
                is_prime = False
                break
        if is_prime:
            if miller_rabin_test(num, 5):
                return num


def main():
    setup = "from prime_num import generate_prime_fix_len"
    times = 10
    i = 8
    while i < 5000:
        print "Length is %d bits: %s" %\
              (i, sum(timeit.repeat('generate_prime_fix_len(%d)'%(i), setup, timeit.default_timer, times, 1)) / times)
        i *= 2
    return

if __name__ == "__main__":
    main()
