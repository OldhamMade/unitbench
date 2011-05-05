'''
Copyright (c) 2011, Joseph LaFata
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the unitbench nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from fractions import gcd
import unitbench
import sys

if sys.version_info >= (3, 0):
    xrange = range

def sieve(n):
    candidates = list(range(n+1))
    fin = int(n**0.5)
    for i in xrange(2, fin+1):
        if not candidates[i]:
            continue
        for k in xrange(2*i, n+1, i):
            candidates[k] = 0
    return [i for i in candidates[2:] if i]
        
def is_prime(p):
    if p == 2:
        return True
    elif p == 3:
        return True
    elif p % 2 == 0 or p % 3 == 0:
        return False
    else:
        top = int(p ** 0.5) + 1
        for i in xrange(6, top, 6):
            if p % (i + 1) == 0 or p % (i - 1) == 0:
                return False
    return True

_default_primes = sieve(1000000)
_default_primes_set = set(_default_primes)
def prime_factors_map(val, primes=_default_primes, pset=_default_primes_set):
    factors = []
    
    next = 0
    count = 0
    index = 0
    while primes[index] <= val:
        if (val % primes[index] == 0):
            next = primes[index]
            count += 1
            val = val / primes[index]
        else:
            if count != 0:
                factors.append((next, count))
                count = 0
            if val in pset:
                factors.append((val, 1))
                break
            index += 1
    else:
        if count != 0:
            factors.append((next, count))
    return factors

def prime_factors_list(val, primes=_default_primes, pset=_default_primes_set):
    factors = []

    index = 0
    while primes[index] <= val:
        if (val % primes[index] == 0):
            factors.append(primes[index])
            val = val / primes[index]
        else:
            if val in pset:
                factors.append(val)
                break
            index += 1
    return factors

def unique_prime_factors_list(val, primes=_default_primes, pset=_default_primes_set):
    factors = []

    index = 0
    while primes[index] <= val:
        if val % primes[index] == 0:
            factors.append(primes[index])
            while val % primes[index] == 0:
                val = val / primes[index]
        else:
            if val in pset:
                factors.append(val)
                break
            index += 1
    return factors

class Totient(unitbench.Benchmark):
    def input(self):
        i = 10
        while i < 1000000:
#        while i < 1000:
            yield i
            i *= 10
            
    def dbench_naive(self, input):
        totient = []
        for n in xrange(input):
            t = 0
            pos = n-1
            while pos > 0:
                if gcd(pos,n) == 1:
                    t += 1
                pos -= 1
            totient.append(t)
            
    def bench_totient(self, input):
        totient = []
        for n in xrange(input):
            if n < 2:
                totient.append(n)
                continue
            t = 1
            for key, value in prime_factors_map(n):
                t *= key ** (value-1) * (key - 1)
            totient.append(t)
#        print totient

    def bench_totient2(self, input):
        totient = []
        for n in xrange(input):
            if n < 2:
                totient.append(n)
                continue
            t = n
            for p in unique_prime_factors_list(n):
                t -= t // p
            totient.append(t)
#        print totient

    def bench_totient3(self, input):
        totient = []
        for n in xrange(input):
            if n < 2:
                totient.append(n)
                continue
            t = n
            for p in unique_prime_factors_list(n):
                t *= (1 - (1.0 / p))
            totient.append(t)
            
if __name__ == "__main__":
    Totient().run()