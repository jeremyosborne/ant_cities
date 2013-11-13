'''
Created on Nov 13, 2013

@author: john
'''
import time

def i_plus_1_for_loop():
    
    t0 = time.clock()    
    for i in range (1, 10000000):
        i = i + 1
    return time.clock() - t0
    
if __name__ == '__main__':
    #Lets test to see if one thing is faster than another.

    t0 = time.clock()    
    for i in range (1, 10000000):
        i = i + 1
    print "i + 1 Benchmark: " + str(time.clock() - t0)
    
        
    t0 = time.clock()    
    for i in range (1, 10000000):
        i += 1
    print "+= Benchmark: " + str(time.clock() - t0)
    
    t0 = time.clock()    
    for i in range (1, 10000000):
        i = i + 1
    print "i + 1 Benchmark: " + str(time.clock() - t0)
    
        
    t0 = time.clock()    
    for i in range (1, 10000000):
        i += 1
    print "+= Benchmark: " + str(time.clock() - t0)
            
    t0 = time.clock()    
    for i in range (1, 10000000):
        i += 1
    print "+= Benchmark: " + str(time.clock() - t0)
    
    t0 = time.clock()    
    for i in range (1, 10000000):
        i = i + 1
    print "i + 1 Benchmark: " + str(time.clock() - t0)
    
        
    t0 = time.clock()    
    for i in range (1, 10000000):
        i += 1
    print "+= Benchmark: " + str(time.clock() - t0)
    
    t0 = time.clock()    
    for i in range (1, 10000000):
        i = i + 1
    print "i + 1 Benchmark: " + str(time.clock() - t0)
    