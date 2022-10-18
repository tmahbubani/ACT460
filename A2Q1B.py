import math
import numpy as np

S = 100
T = 3
r = math.log(1.05)
sigma = 0.3
strike = 105
spot = 100
dt = 1/4
mu = 0.07

# Put: isCall = 0
# Call: isCall = 1
# Linear Combination: isCall = 2
# x is number of calls, y is number of puts

# T is maturity
# dt is timestep

#1 month, 3 mth, 6mth, 1 year timestep. 1,2,3,5 year maturity. P/C/Combo.
# any range of strikes and spots 
# create stock tree array
def main(S,T,r,sigma, mu, strike, dt, isCall, x, y):

    N = T/dt
    up = np.exp(np.sqrt(sigma**2*dt+dt**2*mu**2))     # u
    down = 1/up                        # d
    q=((np.exp(r*dt)-down)/(up-down))  # probability of stock price going up

    # 1 -- Call or European
    # 0 -- Put or American
    # 2 -- linear combination of European and American

    def price(i,j):
        Price = S * (up ** (j - 2*i))
        return Price

    # find option price
    def Premium_Rec(i, j, isCall, isEuropean):
        
        # Compute the exercise profit
        stockPrice = price(i, j)
        
        if isCall == 1:
            exerciseProfit = max(0, stockPrice - strike)
        elif isCall == 2:
            exerciseProfit = x*max(0, stockPrice - strike) + y*max(0, strike - stockPrice)

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

    Price = Premium_Rec(0, 0, isCall, 1)
    return Price

print('The European put option price is:', main(S,T,r,sigma, mu, strike, dt,0, 0, 0))

#19.879622862594708