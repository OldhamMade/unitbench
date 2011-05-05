Getting Started
===============

I tried to design the library to be vary easy to use.  Here
is some simple example code to get you started.

Simple Prime Generation Benchmarks
----------------------------------
.. literalinclude:: ../examples/example.py

Example Console Output
----------------------
.. literalinclude:: results.txt

The default output includes the name of each benchmark.  It is derived from
the name of the function used to generate it.  The user, system, and real times
reported are the averages of the default number of runs (7).

Example CSV Output
------------------
First, changing the output to CSV requires this change:::
  
  if __name__ == "__main__":
      PrimeBenchmark().run(CsvReporter())

Then it produces this output:::

   Values,Naive Primes,Sieve Of Eratosthenes
   100,7.8841602472e-05,2.5209759515e-05
   1000,0.000797913330243,0.000192320436854
   10000,0.010098568763,0.00206587345078
   100000,0.155457692961,0.0319632515729
