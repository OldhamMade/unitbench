API Documentation
=================

This is the documentation for the classes contained in
unitbench.

Benchmark
---------

This is the main class to extend when using unitbench.

.. autoclass:: unitbench.Benchmark
   :members: input, repeats, setup, teardown, warmup
   
   .. method:: run([reporter=None])
      
      If the reporter is None the ConsoleReporter is used.
      
      This should generally not be overloaded.  It runs the benchmark functions
      that are found in the child class.  Benchmark functions are discovered by
      looking for methods starting with **bench**.
   
ConsoleReporter
---------------
This is the default reporter for unitbench.  It will it writes
out results in the following format:

.. literalinclude:: console_doc.txt

.. class:: unitbench.ConsoleReporter
   
   .. method:: __init__([output_stream=sys.stdout])
   
   Will write the output formatted as above to the given file-type
   stream.  It does not open or close the stream, so make sure to
   handle that outside of this method.
   
   The only method called on the stream is write(str), so any object
   with a write function should work.
   
CsvReporter
-----------
This is an alternative reporter for unitbench.  It writes the output
to a csv format for easy ingestion into spreadsheet programs.

.. class:: unitbench.CsvReporter
   
   .. method:: __init__([output_stream=sys.stdout[, time_type="wall"]])
   
   As with the ConsoleReporter this reporter also takes a stream to write its
   output.  It also has a second parameter time_type.  time_type can be "wall",
   "system", or "user".  It denotes which type of time for which to retrieve
   the average.
   
   ======  ==========================
   Type    Definition
   ======  ==========================
   wall    Wall clock time.
   user    User CPU time.
   system  System or kernel CPU time.
   ======  ==========================

Reporter
--------

.. autoclass:: unitbench.Reporter
   :members:

BenchResult
-----------

Using this class is only necessary if you're writing a new
results reporter.  It is passed into the write_results method
of the various reporters.

.. autoclass:: unitbench.BenchResult
   :members: