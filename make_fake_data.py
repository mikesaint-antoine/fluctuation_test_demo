import numpy as np
import random







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





## define params

frac_ON_in_original_population = 0.1

OFF_growth = 1
ON_growth = 1


ON_to_OFF = 0.1

OFF_to_ON = ON_to_OFF / (1/frac_ON_in_original_population -1)


params = [OFF_growth, ON_growth,OFF_to_ON, ON_to_OFF]


# simulate experiment


tend = 6

num_colonies = 100


fracs_ON_in_colonies = []


for count in range(num_colonies):

    draw = random.random()

    if draw <= frac_ON_in_original_population:
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





with open("fake_data.csv", "w") as record_file:
    record_file.write("colony,fraction_ON\n")

    for i in range(len(fracs_ON_in_colonies)):
        # record_file.write("%s\t%s\t%s\n" % (to_write[i][0],to_write[i][1], to_write[i][2]))
        record_file.write(f"colony{i+1},{fracs_ON_in_colonies[i]}\n")










# print(fracs_ON_in_colonies)
# print()
# print()
# print(f"Avg frac ON in colonies: {np.mean(fracs_ON_in_colonies)}")



# CV2 = np.mean(fracs_ON_in_colonies)**2 / np.var(fracs_ON_in_colonies)









