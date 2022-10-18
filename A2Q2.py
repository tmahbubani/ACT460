import math
from re import X
import numpy as np
import sympy as sp
from sympy import symbols, Max
import csv

S = 100
T = 3
N = int(3)
r = 0.05
spot = 100
 
dt = 1
up = 1.2                        # u
down = 0.85                     # d
q=((np.exp(r*dt)-down)/(up-down))  # probability of stock price going up
# discount = np.exp(-r*dt)           # discount factor per one timestep

# create stock tree array

def generate_stock_tree(N,u,d,S):
    stock_tree = np.zeros((N+1,N+1))
    
    for j in range(N+1):
        for i in range(j+1):
            stock_tree[i][j] =S*math.pow(u,j-i)*math.pow(d,i)

    basic_tree = stock_tree

    stock_tree = sp.Matrix(stock_tree)
    a = sp.symbols('a')

    for j in range(N+1):
        for i in range(j+1):
            stock_tree[i,j] = stock_tree[i,j]*a*((1-a)**(j-1))
            
    return basic_tree, stock_tree

def eqn(r, dt,stock_tree,q,spot):
    a = sp.symbols('a')

    f1 = np.exp(-r*dt)*(stock_tree[0,1]*q+stock_tree[1,1]*(1-q))
    f2 = np.exp(-2*r*dt)*(stock_tree[0,2]*q**2+2*stock_tree[1,2]*q*(1-q)+stock_tree[2,2]*(1-q)**2)
    f3 = np.exp(-3*r*dt)*(stock_tree[0,3]*q**3+3*stock_tree[1,3]*q**2*(1-q)+3*stock_tree[2,3]*(1-q)**2*q+stock_tree[3,3]*(1-q)**3)

    A = np.exp(-3*r*dt)*(Max(spot-stock_tree[0,3]/a*(1-a),0)*q**3+3*Max(spot-stock_tree[1,3]/a*(1-a),0)*q**2*(1-q)+3*Max(spot-stock_tree[2,3]/a*(1-a),0)*(1-q)**2*q+Max(spot-stock_tree[3,3]/a*(1-a),0)*(1-q)**3)

    f = np.exp(-r*dt)*f1+np.exp(-2*r*dt)*f2+np.exp(-3*r*dt)*f3-np.exp(-3*r*dt)*A
    return f

def newtons(eqn):

    a = sp.symbols('a')
    f = eqn
    g = f.diff(a)

    xi = 0.5

    for i in range(0,25):
        fans = np.float64(f.evalf(subs = {a:xi}))
        dfans = np.float64(g.evalf(subs = {a:xi}))
        xi = xi - fans/dfans
    return xi

def option_premium(N,stock_tree,a):
    option_tree = np.zeros((N+1,N+1))
    df = np.exp(-r*dt)
    option_tree[:,-1] = np.maximum(100-stock_tree[:,-1]*(1-a)**3,0)

    for j in range(N,0,-1):
        for i in range(j,0,-1):
            option_tree[i-1][j-1] = df * (q*option_tree[i-1][j]+(1-q)*option_tree[i][j])
    
    return option_tree

def delta(stock_tree,option_tree):
    print(stock_tree)
    delta0 = (option_tree[0][1]-option_tree[1][1])/(stock_tree[0][1]-stock_tree[1][1])
    delta1a = (option_tree[0][2]-option_tree[1][2])/(stock_tree[0][2]-stock_tree[1][2])
    delta1b = (option_tree[1][2]-option_tree[2][2])/(stock_tree[1][2]-stock_tree[2][2])
    return delta0, delta1a, delta1b 

stock_tree = generate_stock_tree(N,up,down,spot)
calc = eqn(r,dt,stock_tree[1],q,spot)
a = newtons(calc)
print('root',a)

option_tree = option_premium(3,stock_tree[0],a)
# print(option_tree)

deltas = delta(stock_tree[0], option_tree)

print(deltas)

with open('Q2.csv', 'w') as file_writer:
    writer = csv.writer(file_writer)

    writer.writerow(['Value of a']+[a])
    writer.writerow(['Delta at t=0']+[deltas[0]])
    writer.writerow(['Delta at t=1 if fund up']+[deltas[1]])
    writer.writerow(['Delta at t=1 if fund down']+[deltas[2]])


#edit #1 to be general for all options
#create export to excel file