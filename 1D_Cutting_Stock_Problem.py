import sys
import pandas as pd
import time, numpy as np
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

#Parameters
J = 20 # Number of Cutting patterns = |J|

I = 5 # Number of Items = |I|

range_i = range(0,I)
range_j = range(0,J)

L = 850 # Standard Stock Length

d = [50, 30, 40,42, 20] # d_i

l = [330, 315, 295, 250, 205] # l_i

A = np.array([
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0],
    [1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 2, 0, 1, 0, 0, 1, 0, 1, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 2, 0, 0, 2, 2, 0, 1, 1, 1, 3, 0, 0, 0, 2, 0, 1],
    [1, 0, 1, 1, 0, 4, 1, 0, 0, 1, 1, 1, 1, 0, 2, 2, 2, 1, 0, 2]]) # assignment cost


w = np.zeros(J) # w_j intialized equal to 0

#computer vector of waste
print('Vector of waste associated to cutting patterns j')
for j in range_j:
    count = 0
    for i in range_i:
        count = count + A[i][j]*l[i]
    w[j] = L - count
    print('Waste of patter ',j+1, 'is ', w[j])
    
    
#Create Model
model = pyo.ConcreteModel()

#Define variables
model.x = pyo.Var(range(J), # index j
                  within=Integers, bounds=(0,None))
x = model.x
 
model.C1 = pyo.ConstraintList() # Each task is assigned to exactly one worker.
for i in range_i:
    model.C1.add(expr = sum([A[i][j]*x[j] for j in range_j]) >= d[i])


# Define Objective Function
Total_Stocks = sum(x[j] for j in range_j)
model.obj = pyo.Objective(expr = Total_Stocks, sense = minimize)       
    
begin = time.time()
opt = SolverFactory('cplex')
results = opt.solve(model)

deltaT = time.time() - begin # Compute Exection Duration

model.pprint()

sys.stdout = open("1D_Cutting_Stock_Problem_Results.txt", "w") #Print Results on a .txt file

print('Time =', np.round(deltaT,2))


if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    for j in range_j:
      if pyo.value(x[j]) >= 1.00:
              print('x[',j+1,'] ',pyo.value(x[j]))
    print('Total number of Stock used (Obj Value) =', pyo.value(model.obj))
    
    Total_length = 0
    for i in range_i:
        Total_length = Total_length + d[i]*l[i]
    print('Total length required by items demand: ', Total_length)
    count = 0
    count =np.ceil(Total_length/L)
    print('Minimum number of stock (continuous lower bound):', count)
    
    Total_length = L*pyo.value(model.obj) #compute Total Length of used stocks
    print('Total length of stocks is: ', Total_length)
    
    count = Total_length
    for j in range_j:
        count = count - pyo.value(x[j])*w[j] #Computer Total length used for cut        
    print('Total Length used for cut items is: ', count)    
    print('Total waste is: ', (Total_length - count)) 
    
    for i in range_i:
        count = 0
        for j in range_j:
            count = count + A[i][j] * pyo.value(x[j])
        print("---> Number of Items " , str(i + 1) , " cut is " , count , " out of a demand " , d[i])
              
    print('Solver Status is =', results.solver.status)
    print('Termination Condition is =', results.solver.termination_condition)
    
elif (results.solver.termination_condition == TerminationCondition.infeasible):
   print('Model is unfeasible')
  #print('Solver Status is =', results.solver.status)
   print('Termination Condition is =', results.solver.termination_condition)
   
else:
    # Something else is wrong
    print ('Solver Status: ',  result.solver.status)
    print('Termination Condition is =', results.solver.termination_condition)
    
sys.stdout.close()
