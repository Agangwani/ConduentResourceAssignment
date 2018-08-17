# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 12:47:22 2018

@author: 20800130
"""

import numpy as np
from cvxopt import matrix

x = matrix([12,12,110,120],(2,2))
x = np.transpose(x)
print(x)