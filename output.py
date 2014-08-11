
########################################################################
# lib_lg v0.1                                                          #
# output.py                                                            #
# Joachim de Greeff                                                    #
#                                                                      #
# functions for outputting results                                     #
# eg. plot using Matplotlib or write to file                           #
########################################################################


import numpy as np
import matplotlib.pyplot as plt
import parameters as pm


def plot_DG(data, av_percepts):
    """ Plots average success and average number of percepts
        over the course of multiple discrimination games
    """

    fig, ax1 = plt.subplots()
    
    x = np.arange(1, len(data)+1, 1)
    plt.xlabel("Games")
    
    # plot success on left y-axis
    y = np.array(data)
    ax1.plot(x, y, 'b')
    ax1.set_ylabel("Average success (window=" + str(pm.running_AV) + ")", color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    # plot average percepts right y-axis
    ax2 = ax1.twinx()
    y2 = np.array(av_percepts)
    ax2.plot(x, y2, 'r')
    ax2.set_ylabel("Average number of percepts", color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    
    #plt.ylim([0.0, 1.0])
    plt.show()
