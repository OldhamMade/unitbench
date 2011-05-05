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

from unitbench import Benchmark
import sys

if sys.version_info >= (3, 0):
    xrange = range
    
class PrimeBenchmark(Benchmark):
    
    def input(self):
        """In this example this function is a generator, but
        it could simply return a list of inputs.
        """
        i = 100
        while i <= 100000:
            yield i 
            i *= 10
    
    def bench_naive_primes(self, input):
        primes = []
        for p in xrange(input):
            if p == 2:
                primes.append(p)
            elif p == 3:
                primes.append(p)
            elif p % 2 == 0 or p % 3 == 0:
                continue
            else:
                top = int(p ** 0.5) + 1
                for i in xrange(6, top, 6):
                    if p % (i + 1) == 0 or p % (i - 1) == 0:
                        break
                else:
                    primes.append(p)
        
    def bench_sieve_of_eratosthenes(self, input):
        candidates = list(range(input+1))
        fin = int(input**0.5)
        for i in xrange(2, fin+1):
            if not candidates[i]:
                continue
            for k in xrange(2*i, input+1, i):
                candidates[k] = 0
        return [i for i in candidates[2:] if i]

if __name__ == "__main__":
    PrimeBenchmark().run()