import csv
import numpy as np
import scipy.stats
import sys
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



def grow_colony(init,params,tend):

    OFF_list = [init[0]]
    ON_list = [init[1]]



    OFF_growth = params[0]
    ON_growth = params[1]
    OFF_to_ON = params[2]
    ON_to_OFF = params[3]




    t = [0]


    while t[-1] < tend:
    
        current_OFF = OFF_list[-1]
        current_ON = ON_list[-1]



        props = [OFF_growth * current_OFF , ON_growth * current_ON , OFF_to_ON * current_OFF , ON_to_OFF * current_ON ]


        prop_sum=sum(props);    # total propensitity



        # randomly choose next timepoint
        tau = np.random.exponential(scale=1/prop_sum, size=None)


        # update time
        t.append(t[-1] + tau)




        # choose next event

        # update numbers
        rand2 = random.uniform(0,1)

        # OFF proliferation
        if rand2 * prop_sum <= props[0]:
            OFF_list.append(OFF_list[-1] + 1)
            ON_list.append(ON_list[-1] )



        # ON proliferation
        elif rand2 * prop_sum > props[0] and rand2 * prop_sum <= sum(props[:2]):
            OFF_list.append(OFF_list[-1])
            ON_list.append(ON_list[-1] + 1)


        # OFF to ON switch
        elif rand2 * prop_sum > sum(props[:2]) and rand2 * prop_sum <= sum(props[:3]):
            OFF_list.append(OFF_list[-1] - 1)
            ON_list.append(ON_list[-1] + 1)


        # ON to OFF switch
        elif rand2 * prop_sum > sum(props[:3]) and rand2 * prop_sum <= sum(props[:4]):
            OFF_list.append(OFF_list[-1] + 1)
            ON_list.append(ON_list[-1] - 1)


    # delete last element to prevent overshoot
    t = t[:-1]
    OFF_list = OFF_list[:-1]
    ON_list = ON_list[:-1]




    return( [t , OFF_list, ON_list])






def CV2_from_simulations(gamma, tend, steady_state_frac):


    k = gamma / (1/steady_state_frac - 1) # on rate

    growth_rate = 1




    params = [growth_rate, growth_rate,k, gamma]


    # simulate experiment

    num_colonies = 100


    fracs_ON_in_colonies = []


    for count in range(num_colonies):

        draw = random.random()

        if draw <= steady_state_frac:
            # start with 0 OFF cells, 1 ON cell
            init = [0,1]

            [t_out , OFF_list_out, ON_list_out] = grow_colony(init,params,tend)

            frac = ON_list_out[-1] / (OFF_list_out[-1] + ON_list_out[-1])

            fracs_ON_in_colonies.append(frac)

        else:  
            # start with 1 OFF cell, 0 ON cells
            init = [1,0]
            [t_out , OFF_list_out, ON_list_out] = grow_colony(init,params,tend)

            frac = ON_list_out[-1] / (OFF_list_out[-1] + ON_list_out[-1])

            fracs_ON_in_colonies.append(frac)


    CV2 = np.var(fracs_ON_in_colonies) / np.mean(fracs_ON_in_colonies)**2

    return(CV2)






gamma_guess = random.uniform(0, 5)

CV2 = CV2_from_simulations(gamma_guess, 6, mean_data)




best_gamma = gamma_guess
best_error = (CV2 - CV2_data)**2


for count in range(400):


    print(count)



    gamma_guess = random.uniform(0, 5)

    CV2 = CV2_from_simulations(gamma_guess, 6, mean_data)

    error = (CV2 - CV2_data)**2

    if error < best_error:
        best_gamma = gamma_guess
        best_error = error



print()
print()
print(f"best error: {best_error}")
print(f"best gamma: {best_gamma}")