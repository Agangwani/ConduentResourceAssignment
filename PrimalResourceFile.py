# -*- coding: utf-8 -*-


from cvxopt import matrix, spdiag,spmatrix,sparse,solvers,printing, div, mul
"""
Created on Tue Jul 24 16:01:46 2018

@author: 20800130
"""
"""
Algorithm

Format of the list: 
List[
[Total Users]
[Assignments]
[Tasks]
[Performance Matrix or List in the form of [I1,J1][I1,J2][I2,J1][I2,J2][I3,J1][I3,J2]]
[P matrix of how many tasks each job can complete when assigned]
[List of the demands that are required to be met]
[Cost of overtime (usually a large number so the computer doesn't simply assign people to overtime)]
[Performance of how many tasks each assigned person can do for overtime, usually a row of 1's for test cases]
[solution and backlog can be found through the x and z variables under sol, called through sol['x'] or sol['z']]
]

#Assumptions for Base Program - Assignments and tasks are same number, Ignore the PMatrix to begin with
Test Case:
    List = [users, assignments, tasks, performance, p matrix, required demands, overtime cost, ]
    List = [3, 2, [15,35],[6,8,10,7,9,11],[]]


"""

def primalResourceFile(List):
      
    printing.options['dformat'] = '%.1f'
    printing.options['width'] = -1
# =============================================================================
# #RHS = matrix([1., 1., 1., -15., -15.,0,0,0,0,0,0,0,0], (13,1)) #primal B matrix, dual objective
# # For every element in assignments, append a 1 to the list, for every element in demand, append the demand. 
# # For every row within the CMatrix, append a 0 to the end of the RHS matrix
# # define the number of rows as a counter of how many elements have been appended, and the number of columns as 1
# =============================================================================
    numUsers = List[0]
    numAssign = List[1]
    numTasks = List[2]
    demandRequirement = List[3]
    rhsElementList = []
   
    for x in range(0,numUsers):
       rhsElementList.append(1.)

    for y in range(len(demandRequirement)):
       rhsElementList.append(demandRequirement[y] * -1)

# =============================================================================
#     #CMatrix = matrix([1.,1.,1.,1.,1.,1.,1000.,1000.],(8,1)) 
#     #Primal C matrix, cost of normal assignment
#     # For x in range(numAssign * numUsers) append a 1.0 to the CMatrix,
#     # For every element in demand, append a 1000 to the CMatrix
#     # Define the number of rows as the number of elements in CMatrix and the number of columns set to 1 
#     # Can use a counter to keep track of the number of elements that have been appended to the list
# 
#     #After defining the matrix you edit RHS to add the extra 8 0's to the end of the list and you will have to modify 
#     # the length of the new RHS matrix.
# =============================================================================
    CElements = []
    CCounter = 0
    for x in range((numAssign*numUsers)):
        CElements.append(1.)
        CCounter +=1
    for x in range(numTasks):
        CElements.append(1000)
        CCounter +=1
    CRows = CCounter
    CColumns = 1
    
    CMatrix = matrix(CElements,(CRows,CColumns))
    
    ######
    for a in range(CCounter):
        rhsElementList.append(0)
    rhsRows = len(rhsElementList)
    rhsColumns = 1
    
    RHS = matrix(rhsElementList,(rhsRows,rhsColumns))
    
# =============================================================================
# #UtilizationMatrix = spmatrix([1,1,1,1,1,1],[0,0,1,1,2,2],[0,1,2,3,4,5],(3,6))
# #For x in range(numAssign * numUsers): create a list of 1's: ie spmatrix(list,rowpoints,columnpoints,(numrow,numcolumn))
# # you cannot use a sparse diaganol matrix as the requirement is that
# # each element you're copying must be a square shaped matrix
# #To define the location of each of the element
# #   For each number of jobs, you want to to duplicate the row identifier a certain number of times
# #       I.E. if you have 3 jobs, you want 0,0,0 for the first 3 elements, then 1,1,1, and so forth 
# #   To create the list of columns you simply want to iterate for each element within your list.
# #Create the numberof rows as the length of the of the column identifiers and the rows as: len(rows)/rows[-1]
# =============================================================================
    
    UtilElements = []
    ColIterator = 0
    ColNumber = []

    for x in range((numAssign*numUsers)):
        UtilElements.append(1)
        ColNumber.append(ColIterator)
        ColIterator+=1
    RowNumber = []
    for y in range(numAssign):
        for x in range(numUsers):
            RowNumber.append(x)
    UtilizationMatrix = spmatrix(UtilElements,RowNumber,ColNumber, (numUsers,(numAssign*numUsers)))
    #invalid dimension tuple error because row and column number must be an int, not float
    
    
# =============================================================================
# #DemandMatrix = spmatrix([-6,-8,-10,-7,-9,-11],[0, 0,0,1,1,1],[0,2,4,1,3,5],(2,6))
# # To create the demand matrix you're using the performance matrix and the spmatrix function within cvxopt
# # take your input as the columns first, so for each job, then for each person, append to a list.
# # For the row placements, repeat each row value for every user there is; for 3 users, repeat each value 3 times until 
# # your total number of rows are equal to the number of values in your performance 
# # For your columns, start with 0 and iterate by 2 until you reach the number of iterations is equal to the number of jobs
# # then start from 1 and iterate by 2 until you reach the number of users, and continue the loop while your row 
# # and column matrix are != to the number of elements you're applying 
#     #inputDemand = []
# =============================================================================
# =============================================================================
#     performance = List[4]
#     #PElements = List[5]
#     for x in range(len(performance)):
#         performance[x] = -1 * performance[x]
#     DemandRow = []
#     DemandIterator = 0
#     for x in range(numTasks):
#         for x in range(numUsers):
#             DemandRow.append(DemandIterator)
#         DemandIterator+=1
#     DemandCol = []   
#     DemandIterator = 0
#     #for i in range(int(len(DemandRow)/numUsers)+1):
#     while len(DemandCol) < len(performance):
#         temp = DemandIterator
#         for x in range(int(len(DemandRow)/numTasks)):
#             if(len(DemandCol) == len(performance)):
#                 break;
#             DemandCol.append(temp)
#             temp = temp + numTasks
#         DemandIterator+=1
#         
#    # PMatrix = matrix(PElements,(numAssign,numTasks))
#     DemandMatrix = spmatrix(performance,DemandRow,DemandCol,(numTasks,(numUsers*numAssign)))
# =============================================================================
    
    #DemandMatrix = DemandMatrix * PMatrix
    
# =============================================================================
# Doing the matrix Multiplication:
#     In order to perform matrix multiplication, follow as such. 
#     for x in range(numAssign): 
#         extract the row matrix of your performance as 
#     
#
# =============================================================================
    performance = List[4]
    for x in range(len(performance)):
         performance[x] = -1 * performance[x]
    performMatrix = matrix(performance,(numUsers,numTasks))
    Pmatrixelements = List[5]
    pMatrix = matrix(Pmatrixelements,(numAssign,numTasks))
    holdingarray = []
    for x in range(numAssign):
        newArray = pMatrix[x::numAssign]
        pMatrixAdjust = spdiag(newArray)
        holdingarray.append(pMatrixAdjust)
        print(pMatrixAdjust)
    #matrix multiplication bewtween performance and p matrix
    holding2 = []
    for y in range(len(holdingarray)):
        temp = performMatrix * holdingarray[y]
        holding2.append(temp)
        print(temp)
    demandList = []
    for x in range(len(holding2)):
        temp = holding2[x]
        for x in range(numUsers):
            demandList.append(temp[x::numUsers])
    
    DemandMatrix = matrix(demandList,(numTasks,(numUsers*numAssign)))
    print(DemandMatrix)
        
        
        
# =============================================================================
#     while len(DemandCol) != len(DemandRow):
#         if len(DemandCol) != 0:  
#             DemandCol.append(DemandIteratorPrime)
#         for x in range(int(len(DemandRow)/numAssign)):
#             DemandCol.append(DemandIterator)
#             DemandIterator += 2
#         if len(DemandCol) % numUsers == 0:
#             #DemandIterator = 0 
#             DemandIterator+=1
# =============================================================================
    
    
    
 #"""for x in range(int(len(DemandRow)/numAssign)):
  #          if DemandIteratorPrime % 2 == 0:
   #             DemandCol.append(DemandIterator)
    #            DemandIteratorPrime +=1
     #       else:
      #          DemandCol.append(DemandIteratorPrime)
       #         DemandIteratorPrime += 2
        #DemandIterator+=2
        #DemandIteratorPrime+=1 
        
        #for x in range(int(len(DemandRow)/numAssign)):
        #    DemandCol.append(DemandIteratorPrime)
          #  DemandIteratorPrime+=2 """
    
# =============================================================================
# #BacklogMatrix = spmatrix([-1,-1],[3,4],[0,1],(5,2))
# #To creat the backlog matroix, you want to use the sparsematrix function. your first j job columns and i users rows are
# #full of 0's. then the next j job columns and the num of rows from your demand matrix are going to be a sparsematrix with
# #-1's in a diagonal shape. 
# # You'll place the row starting with -1 after the first i users roles and you can identify the row you want to start as the 
# # numUsers as rows start indexing at 0.  and the first column as 0, from there you simply want to iterate the col by 1.
# =============================================================================
    
    BackLogElements  = []
    
    for x in range(numTasks):
        BackLogElements.append(-1)
    BacklogRow = []
    BacklogCol = []
    BacklogIterator = numUsers
    for x in range(numTasks):
        BacklogRow.append(BacklogIterator)
        BacklogIterator+=1
    BacklogIterator = 0
    for x in range(numTasks):
        BacklogCol.append(BacklogIterator)
        BacklogIterator += 1 
    numRow = numUsers + len(BacklogRow) 
    numCol = numTasks
    
    BacklogMatrix = spmatrix(BackLogElements,BacklogRow,BacklogCol,(numRow,numCol))
    
    
    negIdenList = []
    for x in range((len(UtilizationMatrix)+len(BacklogMatrix))):
        negIdenList.append(-1)
        
    negIden =spdiag(negIdenList)
#Creating the identity matrix is simple, you simply want to a sparse diagonal matrix with as many elements as are in CMat

    AMatrix = sparse([[UtilizationMatrix,DemandMatrix],[BacklogMatrix]])

#simply combining all the elements to make the larger full AMatrix 

    AMatrix = sparse([AMatrix,negIden])
# these are done in separate steps to accomodate with the changing dimensions of each matrix. EDIT in case this doesn't
# work for all test cases, most likely source of error.
#print(AMatrix)
    
    
    solution2 = matrix([0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0],(17,1))

    sol = solvers.lp(CMatrix,AMatrix,RHS)
    
   # print(AMatrix)
    print(sol['x']) # primal variables
 # primal solution, first 6 correspond to assignment, person 1 to task 1, person 1 to task 2,
# final 2 are the backlogs
# first num users doing task 1, next num users doing task 2, next users doing split task

    print(sol['z']) # the dual variables
 # First numUsers values are value of the people, next numTasks are the cost of each new task, goes straight to backlog, ie .125 hours
 #Cost of using backlog high, high 3 values       
     
     #setting up the linear programming assignment process
    assignments = []
    for x in range(numUsers):
        assignments.append(0)
        
    backlog = []
    for x in range(numTasks):
        backlog.append(0)
    
    istar = 0
    jstar = 0
    cost = 0
    exitcount = 0
    counter = 0
    lpo = [numUsers,numAssign,numTasks,[CMatrix,AMatrix,RHS],assignments,backlog,istar,jstar,cost,exitcount,counter]
    
    while(exitcount==0):
        exitcount = iteratePrimal(lpo)
        lpo[6] = istar
        lpo[7] = jstar
        
    


def iteratePrimal(lpo):
    printing.options['dformat'] = '%.1f'
    printing.options['width'] = -1
    numUsers = lpo[0]
    numAssign = lpo[1]
    numTasks = lpo[2]
    CMatrix = lpo[3][0]
    AMatrix = lpo[3][1]
    RHS = lpo[3][2]
    assignment = lpo[4]
    backlog = lpo[5]
    istar = lpo[6]                          
    jstar = lpo[7]
    cost = lpo[8]
    exitcount = lpo[9]
    counter = lpo[10]
    lpsolution = solvers.lp(CMatrix,AMatrix,RHS)
    AMatrix = AMatrix.trans()
    etaIndex = []
    thetaIndex = []
    xIndex = []
    for x in range(numTasks):
        etaIndex.append(numUsers+x)
    for x in range(numUsers):
        thetaIndex.append(x)
    for x in range(numUsers*numAssign):
        xIndex.append(x)
    oldAssign = 0
    oldDemand = RHS[etaIndex]
    #print(oldDemand)
    
    eta = lpsolution['z'][etaIndex]
    
    demand = RHS[etaIndex]
    demand = demand.trans()
    #selection = AMatrix[:,etaIndex]*eta/RHS
    selection = (AMatrix[:,etaIndex]*eta)
    selection = div(selection,CMatrix)
    
    maxnum = 100
    maxIndex = None
    for i in range(len(selection)):
        if selection[i] < maxnum:
            maxnum = selection[i]
            maxIndex = i
    optass = maxIndex
    demand = demand-AMatrix[optass,etaIndex]
    demand = demand.trans()
    RHS[etaIndex] = demand
    if(optass > (numAssign*numUsers)):
        istar = 0
        jstar = optass -(numUsers*numAssign)
        backlog[jstar] = backlog[jstar]+1
    else:
        istar = (optass-1)%(numUsers)+1
        jstar = (optass-istar)/(numUsers)+1
        oldAssign = assignment[istar]
        assignment[istar] = jstar
        unassigned = []
        for z in range(numTasks):
            for y in range(numAssign):
                for x in range(len(assignment)):
                    unassigned.append(assignment[x]==0)
        unassignedMatrix = matrix(unassigned,(int(len(unassigned)/2),numTasks))
        AMatrix[xIndex,etaIndex] = mul(AMatrix[xIndex,etaIndex],unassignedMatrix)
    cost = cost+CMatrix[optass]
    counter = counter+1
    if(max(demand)>=0):
        exitcount = 1
    if oldAssign >0:
        exitcount = 3
    if(max(oldDemand)>max(demand)):
        exitcount = 4
    
    print(assignment)
    return exitcount    
        
        
    

    
    
    
def main():
    #inputList = numUsers, numAssign,numtasks, demand, performance(per task), P Matrix
    inputList =[5,3,2,[15,35],[6,8,10,8,16,12,10,20,14,10],[1,0,0.5,0,1,0.5]] 
    # performance should be numUser*numAssign long 
    sol = primalResourceFile(inputList)
    #print(sol)
    
main()

