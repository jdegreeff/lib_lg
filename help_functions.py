
########################################################################
# lib_lg v0.1                                                          #
# help_functions.py                                                    #
# Joachim de Greeff                                                    #
#                                                                      #
# various helper functions                                             #
########################################################################

import math, random
import data


def calc_euclidean_distance(x, y):
    """ euclidean distance between x and y
    """
    if len(x) != len(y):
        raise ValueError, "vectors must be same length"
    total = 0
    for i in range(len(x)):
        total += ( x[i] -y[i])**2
    return math.sqrt(total)


def calc_running_average_list(item_list, window):
    """ calculates running average over a given list and window
        returns -1 if list is empty
    """
    
    if(len(item_list) < window ):
        window = len(item_list)
        
    if (window > 0):
        tmp_list = item_list[ len(item_list)-window:len(item_list)]
        return sum(tmp_list)/(1.0*window)
    else:
        return -1
    
    
def generate_context(n_dimensions, context_size, object_distance, max_retries):
    """ generates a context for given dimensions and context size
        objects in the context are at minimum distance (parameters.object_distance) from each other
    """
    if context_size == 1:
        return [[ random.random() for _ in xrange(n_dimensions) ]]
    
    min_dist = math.sqrt(n_dimensions * (object_distance**2))
    tmp_context = [[ random.random() for _ in xrange(n_dimensions) ]]
    
    counter = 0
    while (len(tmp_context) < context_size) and (counter < max_retries):
        counter += 1
        new_percept = [ random.random() for _ in xrange(n_dimensions) ]
        distances = [ calc_euclidean_distance(i, new_percept) for i in tmp_context ]
        if min(distances) < min_dist:
            pass
        else:
            tmp_context.append(new_percept)
    
    if counter == max_retries:
        raise Exception("Could not generate context in " + str(max_retries) + " retries")
    else:
        return tmp_context
    
    
def calc_average(list_of_lists):
    """ calculates average and SD for a given list of lists containing numbers
        lists are assumed to be of same length
    """
    average_list = []
    for i in range(len(list_of_lists[0])):
        av = []
        for j in list_of_lists:
            av.append(j[i])
        average_list.append(sum(av)/(1.0*len(list_of_lists)))
    return average_list
    
    
    
def generateRandomWord(lexicon, length):
    """ generates a random word with a given length
        generated word is not in the provided lexicon
    """
    check = False
    while not check:
        i = 0
        word = ""
        while i < length :
            if i % 2 == 0:
                word += str(random.choice(data.consonant_set))
            else:
                word += str(random.choice(data.vowel_set))
            i += 1
        if word not in lexicon:   #check if word is unique
            check = True
    return word
    
    
