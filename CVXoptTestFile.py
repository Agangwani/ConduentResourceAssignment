# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:52:13 2018

@author: 20800130
"""

from cvxopt import matrix, solvers, spmatrix, sparse,spdiag

backlog = spmatrix([0],[0],[0],(3,2))
print(matrix(backlog))

B = spmatrix([-1,-1,-1,-1,-1,-1],[0,0,1,1,2,2],[0,1,2,3,4,5],(3,6))
print(matrix(B))

DConstraint = spmatrix([6,7,8,9,10,11],[0,1,0,1,0,1],[0,1,2,3,4,5],(2,6))

print(matrix(DConstraint))

E = matrix([[1,0],[0,1]])
print(matrix(E))

FinalAMatrix = sparse([[B,DConstraint],[backlog,E]])
print(matrix(FinalAMatrix))

FinalBMatrix = matrix([[-1,-1,-1,15,35]])
print(matrix(FinalBMatrix))

FinalCMatrix = matrix([1,1,1,1,1,1,2,2],(8,1))
print(FinalCMatrix)

sol = solvers.lp(FinalCMatrix,FinalAMatrix,FinalBMatrix)
