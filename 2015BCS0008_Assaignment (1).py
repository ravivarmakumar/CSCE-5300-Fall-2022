#######################################################################
#        This is implementation of sieve of erathosthenes            #
# Using Parallel Programming via mpi4py module on the platform PYTHON #
#         You have to change the input of needed              #
#######################################################################
from mpi4py  import MPI                        		# Importing the module MPI from mpi4py
import math                            			# For mathematical Caluclations
n = 100000                                      	# Calculating number of primes less than this number
Input=[]
Processors_size = MPI.COMM_WORLD.Get_size()            	# Determines the number of processors
Processors_rank = MPI.COMM_WORLD.Get_rank()            	# Determines rank of each processor
div=n/(Processors_size-1)                    		# Divides the work among the processors
div=int(div)
temp=[]
i=1
while i<Processors_size:
   temp.append(div*i)
   i=i+1
Processors_id=1
if Processors_rank==0:
   i=2
   while i<int(math.sqrt(n))+1:
      temp_0=1
      j=2
      while j<int(math.sqrt(i))+1:
           if  i%j==0:
               temp_0=0     
               break
           j=j+1
      if temp_0==1:             
               Input.append(i)
      p=0
      while p<Processors_size-1:
               if i==int(math.sqrt(temp[p])):                                                                   
                   MPI.COMM_WORLD.send(Input, dest=Processors_id)    # Sends the exact count of elements
                   Processors_id=Processors_id+1
                   break
               p=p+1
      i=i+1
Length_Input=len(Input)
temp_id=1
temp_1=[]
while temp_id<Processors_size :   
   if Processors_rank==temp_id:
         temp_2=[]
         temp_2= MPI.COMM_WORLD.recv(source=0)                # Recieves at most count of elements
         Length_Input=len(temp_2))
         if(Processors_rank==1):
            r=0
            while r<len(temp_2):
               a=temp_2[r]
               temp_1.append(a)
               r=r+1
         i=(temp_id-1)*div+1
         while i<(temp_id*div):
               temp_0=1
               k=0
               while k<Length_Input: 
                   if i%temp_2[k]==0:
                       temp_0=0
                       break
                   k=k+1
               if (temp_0==1)and(i!=1):
                  temp_1.append(i)
               i=i+2
   temp_id=temp_id+1
Output=[]
Output = MPI.COMM_WORLD.gather(temp_1, root=0)                # Gathers all the outputs of each processor and finalises the output
if Processors_rank==0:
  print(Output)
