# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:42:19 2018

@author: 20800130
"""
import numpy as np
from cvxopt import matrix, printing, solvers, spdiag, sparse,spmatrix

numTasks = 2
numAssign = 3
Pmatrixelements = [1,0,0.5,0,1,0.5]
pMatrix = matrix(Pmatrixelements,(numAssign,numTasks))
print(pMatrix)
x = 0
newArray = pMatrix[:,0]
print(newArray)