# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:03:02 2018

@author: 20800130
"""
import numpy as np
from cvxopt import matrix, printing, solvers, spdiag, sparse,spmatrix

# Needed in order to properly format matricies for analysis

printing.options['dformat'] = '%.1f'
printing.options['width'] = -1



RHS = matrix([1., 1., 1., -15., -15.,0,0,0,0,0,0,0,0], (13,1)) 
#primal B matrix, dual objective
# For every element in assignments, append a 1 to the list, for every element in demand, append the demand. 
# For every row within the CMatrix, append a 0 to the end of the RHS matrix
# define the number of rows as a counter of how many elements have been appended, and the number of columns as 1

#print(RHS)

CMatrix = matrix([1.,1.,1.,1.,1.,1.,1000.,1000.],(8,1)) 
#Primal C matrix, cost of normal assignment
# For x in range(numAssign * numUsers) append a 1.0 to the CMatrix,
# For every element in demand, append a 1000 to the CMatrix
# Define the number of rows as the number of elements in CMatrix and the number of columns set to 1 
# Can use a counter to keep track of the number of elements that have been appended to the list

#After defining the matrix you edit RHS to add the extra 8 0's to the end of the list and you will have to modify 
# the length of the new RHS matrix.

#print(CMatrix)


UtilizationMatrix = spmatrix([1,1,1,1,1,1],[0,0,1,1,2,2],[0,1,2,3,4,5],(3,6))
#For x in range(numAssign * numUsers): create a list of 1's: ie spmatrix(list,rowpoints,columnpoints,(numrow,numcolumn))
# you cannot use a sparse diaganol matrix as the requirement is that
# each element you're copying must be a square shaped matrix
#To define the location of each of the element
#   For each number of jobs, you want to to duplicate the row identifier a certain number of times
#       I.E. if you have 3 jobs, you want 0,0,0 for the first 3 elements, then 1,1,1, and so forth 
#   To create the list of columns you simply want to iterate for each element within your list.
#Create the numberof rows as the length of the of the column identifiers and the rows as: len(rows)/rows[-1]

DemandMatrix = spmatrix([-6,-8,-10,-7,-9,-11],[0,0,0,1,1,1],[0,2,4,1,3,5],(2,6))
# To create the demand matrix you're using the performance matrix and the spmatrix function within cvxopt
# take your input as the columns first, so for each job, then for each person, append to a list.
# For the row placements, repeat each row value for every user there is; for 3 users, repeat each value 3 times until 
# your total number of rows are equal to the number of values in your performance 
# For your columns, start with 0 and iterate by 2 until you reach the number of iterations is equal to the number of jobs
# then start from 1 and iterate by 2 until you reach the number of users, and continue the loop while your row 
# and column matrix are != to the number of elements you're applying 


#print(DemandMatrix)

BacklogMatrix = spmatrix([-1,-1],[3,4],[0,1],(5,2))
#To creat the backlog matroix, you want to use the sparsematrix function. your first j job columns and i users rows are
#full of 0's. then the next j job columns and the num of rows from your demand matrix are going to be a sparsematrix with
#-1's in a diagonal shape. 
# You'll place the row starting with -1 after the first i users roles and you can identify the row you want to start as the 
# numUsers as rows start indexing at 0.  and the first column as 0, from there you simply want to iterate the col by 1.

#print(BacklogMatrix)

negIden =spdiag([-1,-1,-1,-1,-1,-1,-1,-1])
#Creating the identity matrix is simple, you simply want to a sparse diagonal matrix with as many elements as are in CMat

AMatrix = sparse([[UtilizationMatrix,DemandMatrix],[BacklogMatrix]])

#simply combining all the elements to make the larger full AMatrix 

AMatrix = sparse([AMatrix,negIden])
# these are done in separate steps to accomodate with the changing dimensions of each matrix. EDIT in case this doesn't
# work for all test cases, most likely source of error.
#print(AMatrix)

sol = solvers.lp(CMatrix,AMatrix,RHS)

print(sol['x'])
 # primal solution, first 6 correspond to assignment, person 1 to task 1, person 1 to task 2,
# final 2 are the backlogs


print(sol['z'])
 # First 3 values are value of the people, next two are the cost of each task, ie .125 hours
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