import csv
import numpy as np
import scipy.stats
import sys
import math
import random




## reading in data
data = []
with open("fake_data.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:

        # print(row)
        # input()


        data.append(float(row[1]))



# print(data)

mean_data = np.mean(data)
var_data = np.var(data)

CV2_data = var_data / mean_data**2

print(f"mean of fractions: {mean_data}")
print(f"variance of fractions: {var_data}")
print(f"CV^2 of fractions: {CV2_data}")




######################################################################################################
######################################################################################################
######################################################################################################





def CV2_formula(gamma, t, steady_state_frac):

    k = gamma / (1/steady_state_frac - 1) # on rate

    r = 1

    E = math.e

    numerator = gamma* ( -2 * r * E**(t *( r-2*(gamma+k) )) + 2*gamma + 2*k + r )

    denomenator = k * (2*E**(r*t) - 1) * (2*(gamma+k) - r)

    CV2 = numerator / denomenator

    return(CV2)




gamma_guess = random.uniform(0, 5)

CV2 = CV2_formula(gamma_guess, 6, mean_data)




best_gamma = gamma_guess
best_error = (CV2 - CV2_data)**2


for count in range(10000):


    gamma_guess = random.uniform(0, 5)

    CV2 = CV2_formula(gamma_guess, 6, mean_data)

    error = (CV2 - CV2_data)**2

    if error < best_error:
        best_gamma = gamma_guess
        best_error = error



print()
print()
print(f"best error: {best_error}")
print(f"best gamma: {best_gamma}")

