#import modules
import sys
import numpy as np
import math as mt
import random

#import mpi modules
import mpi4py
from mpi4py import MPI

#declaring env variables like rank and size of processors
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#taking input from user for total number of numbers in the array
N = int(sys.argv[1])
#dividing into chunks 
chunk = int(N/size)
#getting random numbers in the range of 1 to 1_000_000
randomnums = random.sample(range(1,N*10),N)

#function that will return the least,highest primes in the array
def prime(arr):
	max_val = max(arr)
	prime = [True for i in range(max_val+1)] #initial boolean list taking all as primes
	prime[0] = False #number 0
	prime[1] = False #number 1

	for p in range(2,mt.ceil(mt.sqrt(max_val))):
		if prime[p] == True:
			for i in range(2*p,max_val+1,p): #if it is multiples of the same number, then changing the flag to False as it is not a prime
				prime[i] = False
	minimum = 10**9
	maximum = -10**9

	for i in range(len(arr)):
		if prime[arr[i]] == True:
			minimum = min(minimum,arr[i])
			maximum = max(maximum,arr[i])
	
	return minimum,maximum

#base values of the results array
result = (1,2)

#creating zeros array with the chunk size
worker_chunk = [0]*(chunk)
worker_part = [0]*(chunk)

#intializing buffers to store each worker results
worker_buffer = []
result_buffer = []
master_buffer = []

i=1

#master
if rank==0:
    #divide total work into equal chunks with each chunk size of N/P
    while i < size:
        #create slices for start and stop indices for array slice for each worker
        start = i*chunk
        end = (i+1)*chunk
        #slicing the worker chunk from initial array
        worker_part = randomnums[start:end]
        #sending worker parts to each worker
        comm.send(worker_part, dest=i, tag=20)
        #recieve result from each worker
        result_buffer = result_buffer + comm.recv(source=i, tag=10)
        i = i+1

#worker
else:
    #receive work from master
    worker_chunk = comm.recv(source=0, tag=20)
    #call the prime function on the sliced chunk passed to workers
    worker_min,worker_max = prime(worker_chunk)
    worker_buffer = list([worker_min,worker_max])
    #send result to master
    comm.send(worker_buffer, dest=0, tag=10)

#master calls all results of workers and it's work to calculate output
if rank == 0:
    master_min,master_max = prime(randomnums[0:chunk])
    master_buffer = list([master_min,master_max])
    output = master_buffer + result_buffer
    output = [*set(output)]
    if len(output) == 2:
    	print("No Primes in the Selected Range")
    elif len(output) > 2:
    	output.remove(min(output))
    	output.remove(max(output))
    	print("Number of Processor cores = ",size)
    	print("Total numbers in the array =",N)
    	print("Minimum Prime Number = ", min(output))
    	print("Maximum Prime Number = ", max(output))
