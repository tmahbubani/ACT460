import math
import numpy as np
import csv

S = 100
T = 3
r = math.log(1.05)
sigma = 0.3
strike = 105
spot = 100
dt = 1/4
mu = 0.07

# TO CALL THIS FUNCTION. If you are finding either a call or a put, the function input can be normal int/float values
# for example: TotalPrice = main(S,T,r,sigma, mu, strike, dt,0,1)
# if you are finding a linear combination of options, the function inputs must be in list form
# for example:TotalPrice = main([S1,S2],[T1,T2],[r1,r2],[sigma,sigma], [mu,mu], [strike,strike, [dt,dt],[0,0],[1,0])

# I assumed that all variables could be different for all options which is why they all have list inputs.
#  I believe that usually variables that relate to the underlying asset, such as spot price, would 
#  be the same for all options, but I left these customizable in case the TA wanted to change these across options as well.

# For my Excel, I am currently outputting the option price from part A, with the different
# time steps, maturities, and option types listed in the question.

# dt should be inputted in terms of years.

# Different examples of options with a specific maturity, dt, and option type is exported to a csv right now.
# Other examples are available in the commented out lines at the bottom of my code. I did not export
# all of them at once because it would take a while to run on the TA's computer due to the high level of computation.

def main(S,T,r,sigma, mu, strike, dt, isCall, isEuropean):

    def indiv(S,T,r,sigma, mu, strike, dt, isCall, isEuropean):

        N = T/dt
        up = np.exp(np.sqrt(sigma**2*dt+dt**2*mu**2))     # u
        down = 1/up                        # d
        q=((np.exp(r*dt)-down)/(up-down))  # probability of stock price going up

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

        Price = Premium_Rec(0, 0, isCall, isEuropean)
        return Price
    
    TotalPrice = 0

    if type(strike) is list:
        for i in range(0,len(strike)):
            TotalPrice += indiv(S[i],T[i],r[i],sigma[i], mu[i], strike[i], dt[i], isCall[i], isEuropean[i])

    else:
        TotalPrice = indiv(S,T,r,sigma, mu, strike, dt, isCall, isEuropean)

    return TotalPrice

O1 = main(S,1,r,sigma, mu, strike, 1/12,0,1)
# O2 = main(S,2,r,sigma, mu, strike, 1/12,0,1)
# O3 = main(S,3,r,sigma, mu, strike, 1/12,0,1)
# O4 = main(S,5,r,sigma, mu, strike, 1/12,0,1)

# O5 = main(S,1,r,sigma, mu, strike, 1/4,0,1)
# O6 = main(S,2,r,sigma, mu, strike, 1/4,0,1)
# O7 = main(S,3,r,sigma, mu, strike, 1/4,0,1)
# O8 = main(S,5,r,sigma, mu, strike, 1/4,0,1)

# O9 = main(S,1,r,sigma, mu, strike, 1/2,0,1)
# O10 = main(S,2,r,sigma, mu, strike, 1/2,0,1)
# O11 = main(S,3,r,sigma, mu, strike, 1/2,0,1)
# O12 = main(S,5,r,sigma, mu, strike, 1/2,0,1)

# O13 = main(S,1,r,sigma, mu, strike, 1,0,1)
# O14 = main(S,2,r,sigma, mu, strike, 1,0,1)
# O15 = main(S,3,r,sigma, mu, strike, 1,0,1)
# O16 = main(S,5,r,sigma, mu, strike, 1,0,1)

A1 = main(S,1,r,sigma, mu, strike, 1/12,1,1)
# A2 = main(S,2,r,sigma, mu, strike, 1/12,1,1)
# A3 = main(S,3,r,sigma, mu, strike, 1/12,1,1)
# A4 = main(S,5,r,sigma, mu, strike, 1/12,1,1)

# A5 = main(S,1,r,sigma, mu, strike, 1/4,1,1)
# A6 = main(S,2,r,sigma, mu, strike, 1/4,1,1)
# A7 = main(S,3,r,sigma, mu, strike, 1/4,1,1)
# A8 = main(S,5,r,sigma, mu, strike, 1/4,1,1)

# A9 = main(S,1,r,sigma, mu, strike, 1/2,1,1)
A10 = main(S,2,r,sigma, mu, strike, 1/2,1,1)
# A11 = main(S,3,r,sigma, mu, strike, 1/2,1,1)
# A12 = main(S,5,r,sigma, mu, strike, 1/2,1,1)

# A13 = main(S,1,r,sigma, mu, strike, 1,1,1)
# A14 = main(S,2,r,sigma, mu, strike, 1,1,1)
# A15 = main(S,3,r,sigma, mu, strike, 1,1,1)
# A16 = main(S,5,r,sigma, mu, strike, 1,1,1)

A17 = main([S,S],[1,1],[r,r],[sigma,sigma], [mu,mu], [strike,strike], [1/4,1/4],[0,1],[1,1])

with open('Q1B.csv', 'w') as file_writer:
    writer = csv.writer(file_writer)
    writer.writerow(['Maturity = 1 year. Put. dt = 1 month'] + [O1])
    writer.writerow(['Maturity = 2 years. Call. dt = 12  months'] + [A10])
    writer.writerow(['Maturity = 1 year each. Call and put. dt = 3 months'] + [A17])
