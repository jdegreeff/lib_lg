
########################################################################
# lib_lg v0.1                                                          #
# agent.py                                                             #
# Joachim de Greeff                                                    #
#                                                                      #
# agents and Conceptual Space representation                           #
########################################################################



import operator
import numpy as np
import help_functions as hp
import parameters as pm



class Agent():
    """ Agent
    """
    
    def __init__(self, name, learning=True):
        self.agent_name = name
        self.learning = learning    # specifies if the agent is learning; typically a teaching agent will not learn
        self.cs = CS()
        self.dg_success = []
        self.dg_running_av = []
        self.dg_n_percepts = []
        
        
        
    def calculate_RA_DG(self):
        """ calculates DG success based on running average
        """
        latest_RA = hp.calc_running_average_list(self.dg_success, pm.running_AV)
        self.dg_running_av.append(latest_RA)
        return self.dg_running_av[-1]
        
        

class CS():
    """ Conceptual Space containing percepts, lexicon and connection matrix
    """
    
    def __init__(self):
        self.percepts = {}
        self.lexicon = []
        #self.matrix = np.array()
        
        
    def get_best_match(self, point):
        """ returns best matching percept tag for given point
        """
        distance = 9999999999999999999999999999
        best_match = ""
        for i in self.percepts.keys():
            dist = hp.calc_euclidean_distance(point, self.percepts[i])
            if dist < distance:
                distance = dist
                best_match = i
        return best_match
    
    
    def shift_percept(self, percept_tag, point):
        """ shifts provided percept towards provided point
        """
        coors = self.percepts[percept_tag]
        diff = [pm.learning_rate * x for x in map(operator.sub, coors, point)]
        self.percepts[percept_tag] = map(operator.add, coors, diff)        
        #meaning{a}(m(t),:) = closest + LEARNINGRATE * ( c(t,:) - closest );
                    

        
        
        
        