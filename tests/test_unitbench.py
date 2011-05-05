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
import sys
from nose.tools import assert_almost_equals, eq_
from unitbench import TimeSet, Benchmark, BenchResult, Reporter, CsvReporter
from unittest import TestCase

if sys.version_info < (3, 0):
    from StringIO import StringIO
else:
    from io import StringIO

class NullReporter(Reporter):
    pass

class OneRun(Benchmark):
    def warmup(self):
        return 0
    
    def repeats(self):
        return 1

class TestBenchResult(TestCase):
    
    def test_stats(self):
        times = []
        times.append(TimeSet(3, 1, 0))
        times.append(TimeSet(4, 2, 0))
        times.append(TimeSet(4, 4, 0))
        times.append(TimeSet(5, 5, 0))
        times.append(TimeSet(6, 7, 0))
        times.append(TimeSet(8, 11, 0))
        
        results = BenchResult("bench_sample1", 10, times)
        
        eq_(results.name, "bench_sample1")
        assert results.value == "10"
        
        assert results.wall_min == 3
        assert results.wall_max == 8
        assert results.wall_mean == 5
        assert_almost_equals(results.wall_variance, 2.67, places=2)
        assert_almost_equals(results.wall_stddev, 1.63, places=2)
        
        assert results.user_min == 1
        assert results.user_max == 11
        assert results.user_mean == 5
        assert results.user_variance == 11.0
        assert_almost_equals(results.user_stddev, 3.32, places=2)

class TestBenchmark(TestCase):
    def test_warmup(self):
        class sample(Benchmark):
            def __init__(self):
                self.count = 0
                self.count2 = 0
                
            def warmup(self):
                return 4
            
            def repeats(self):
                return 0
            
            def bench_count(self):
                self.count += 1
                
            def bench_count2(self, input):
                self.count2 += 1
            
        bm = sample()
        bm.run(NullReporter())
        assert bm.count == 4
        assert bm.count2 == 4
            
    def test_teardown(self):
        """ teardown should be called regardless of errors
        """
        class sample(Benchmark):
            def __init__(self):
                self.setup_count = 0
                
            def setup(self):
                self.setup_count += 1
                if self.setup_count > 1:
                    raise ValueError
            
            def teardown(self):
                self.setup_count -= 1
                if self.setup_count < 0:
                    raise ValueError
                
            def bench_exception(self, input):
                1/0
                
            def bench_works(self):
                pass
        
        bm = sample()
        self.assertRaises(ZeroDivisionError, bm.run)
        
        assert bm.setup_count == 0
        
    def test_input(self):
        class SampleBase(OneRun):
            def __init__(self):
                self.passed_in = []
                
            def bench_sample(self, input):
                self.passed_in.append(input)
        
        class InputGen(SampleBase):
            def input(self):
                i = 10
                while i < 1000:
                    yield i
                    i *= 10
                    
        class InputList(SampleBase):
            
            def input(self):
                return [10, 100, 1000, 20]
            
        bm = InputGen()
        bm.run(NullReporter())
        
        assert bm.passed_in == [10, 100]
        
        bm = InputList()
        bm.run(NullReporter())
        
        assert bm.passed_in == [10, 100, 1000, 20]
        
    def test_param_count(self):
        class sample(OneRun):
            def bench_no_params(self):
                self.no_param = True
            
            def bench_one_param(self, input):
                self.one_param = True
                
        bm = sample()
        bm.run(NullReporter())
        
        assert bm.no_param
        assert bm.one_param
        
    def test_findbenchmarks(self):
        class sample(Benchmark):
            
            def benchSample1(self, input):
                pass
            
            def bench_Sample2(self, input):
                pass
            
            def sampleBench3(self, input):
                pass
            
            def bench_sample4(self):
                pass
                
        bms = sample()._find_benchmarks()
        assert "benchSample1" in bms
        assert "bench_Sample2" in bms
        assert not "sampleBench3" in bms
        assert "bench_sample4" in bms
        
    def test_function_name_to_title(self):
        bm = OneRun()
        eq_(bm._function_name_to_title("bench_sample1_sample2"), "Sample1 Sample2")
        eq_(bm._function_name_to_title("benchSample1Sample2"), "Sample1 Sample2")
        eq_(bm._function_name_to_title("sample1_sample2"), "Sample1 Sample2")
        eq_(bm._function_name_to_title("Sample1Sample2"), "Sample1 Sample2")
        eq_(bm._function_name_to_title("_sample1_sample2_"), "Sample1 Sample2")
        eq_(bm._function_name_to_title("XMLBenchmark"), "Xml Benchmark")
        
class TestCsvReporter(TestCase):
    def test_write_titles(self):
        class sample(OneRun):
            def warmup(self):
                return 0
            
            def repeats(self):
                return 0
            
            def bench_sample1(self):
                self.no_param = True
            
            def bench_sample2(self, input):
                self.one_param = True
                
        bm = sample()
        
        stream = StringIO()
        bm.run(CsvReporter(stream))
        
        output = stream.getvalue()
        stream.close()
        
        eq_("Values,Sample1,Sample2\n", output)
        
        
        