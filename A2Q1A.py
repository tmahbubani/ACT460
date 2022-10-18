import math
import numpy as np
import csv

S = 100
T = 3
N = int(3)*4
r = math.log(1.05)
sigma = 0.3
mu = 0.07
strike = 105
spot = 100
 
dt = 1/4
up = np.exp(np.sqrt(sigma**2*dt+dt**2*mu**2))     # u
down = 1/up                        # d
q=((np.exp(r*dt)-down)/(up-down))  # probability of stock price going up
discount = np.exp(-r*dt)           # discount factor per one timestep

# create stock tree array

def generate_stock_tree(N,u,d,S):
    stock_tree = np.zeros((N+1,N+1))
    
    for j in range(N+1):
        for i in range(j+1):
            stock_tree[i][j] = S*math.pow(u,j-i)*math.pow(d,i)
            
    return stock_tree

# find payoff
def payoff(spot,K,iscall):
    if iscall == 1:
        payoff = max(spot-K,0)
    else:
        payoff = max(K-spot,0)
     
    return payoff

# visualize option payoff tree
def option_premium(N,stock_tree,K,q,df,iscall,isEuropean):
    option_tree = np.zeros((N+1,N+1))
    
    if iscall == 1:
        option_tree[:,-1] = np.maximum(stock_tree[:,-1]-K,0)
    else:
        option_tree[:,-1] = np.maximum(K-stock_tree[:,-1],0)
        
    for j in range(N,0,-1):
        for i in range(j,0,-1):
            if isEuropean == 1:
                option_tree[i-1][j-1] = df * (q*option_tree[i-1][j]+(1-q)*option_tree[i][j])
            else:
                option_tree[i-1][j-1] = max(df * (q*option_tree[i-1][j]+(1-q)*option_tree[i][j]),
                                                payoff(stock_tree[i-1][j-1],K,iscall))
    
    return option_tree


# 1 -- Call or European
# 0 -- Put or American

def price(i,j):
    Price = S * (up ** (j - 2*i))
    return Price

# find option price
def Premium_Rec(i, j, isCall, isEuropean):
    
    # Compute the exercise profit
    stockPrice = price(i, j)
    
    if isCall == 1:
        exerciseProfit = max(0, stockPrice - strike)
    else:
        exerciseProfit = max(0, strike - stockPrice)

    # Base case (this is a leaf)
    if j == N: return exerciseProfit

    # Recursive case: compute the binomial value
    df = math.exp(-r * dt)
    expected = q * Premium_Rec(i, j + 1, isCall, isEuropean) + (1 - q) * Premium_Rec(i + 1, j + 1, isCall, isEuropean)
    binomial = df * expected
    
    if isEuropean == 1: # European Option
        return binomial
    else: # American Option
        return max(binomial, exerciseProfit)

stock_tree = generate_stock_tree(N,up,down,spot)
PutOptionTree = option_premium(N,stock_tree,strike,q,discount,0,1)
PutPrice = Premium_Rec(0, 0, 0, 1)


print('The European Put option premium tree is:\n',np.round(PutOptionTree,decimals = 1))
print('The European put option price is:', PutPrice)

with open('Q1A.csv', 'w') as file_writer:
    writer = csv.writer(file_writer)

    writer.writerow(['Binomial tree'])
    for item in PutOptionTree:
        writer.writerow(item)

    writer.writerow(['Put price'] + [PutPrice])
