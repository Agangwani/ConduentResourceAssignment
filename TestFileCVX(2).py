# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:03:02 2018

@author: 20800130
"""
import numpy as np
from cvxopt import matrix, printing, solvers, spdiag, sparse,spmatrix
from contextlib import suppress


RHS = matrix([1., 1., 1., -15., -10000.,0,0,0,0,0,0,0,0], (13,1)) # primal B matrix, dual objective

#print(ObjMat)

CMatrix = matrix([1.,1.,1.,1.,1.,1.,1000.,1000.],(8,1)) #Primal C matrix, cost of normal assignment


#print(CMatrix)

UtilizationMatrix = spmatrix([1,1,1,1,1,1],[0,0,1,1,2,2],[0,1,2,3,4,5],(3,6))


DemandMatrix = spmatrix([-6,-8,-10,-7,-9,-11],[0,0,0,1,1,1],[0,2,4,1,3,5],(2,6))
print(DemandMatrix)

BacklogMatrix = spmatrix([-1,-1],[3,4],[0,1],(5,2))
print(BacklogMatrix)

negIden = spmatrix([-1,-1,-1,-1,-1,-1,-1,-1],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],(8,8))

AMatrix = sparse([[UtilizationMatrix,DemandMatrix],[BacklogMatrix]])

AMatrix = sparse([AMatrix,negIden])
print(AMatrix)

sol = solvers.lp(CMatrix,AMatrix,RHS,)

print(sol['x']) # primal solution, first 6 correspond to assignment, person 1 to task 1, person 1 to task 2, final 2 are the backlogs


print(sol['z']) # First 3 values are value of the people, next two are the cost of each task, ie .125 hours
"""
#print(performance4)
#print(performance1)
#print(backlogCostMat)

#TotalPerformance = sparse([performance1,performance2,performance3,performance4,backlogCostMat])
#print(TotalPerformance)
#X = sparse([[E],[TotalPerformance]])
#X = X.trans()

#sol = solvers.lp(ObjMat,X,CMatrix)

#sol = solvers.lp(ObjMat,X,CMatrix)

print(sol['x'])

#DualMatrix = spmatrix([dualmatrixinsert],[0,1,2,3,4,)
"""