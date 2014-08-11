
import operator
import numpy as np
import help_functions as hp



class Agent():
    """ Agent
    """
    
    def __init__(self, name, parameters):
        self.agent_name = name
        self.pm = parameters
        self.dg_success = []
        self.dg_running_av = 0
        self.cs = CS(self.pm)
        
        
    def calculate_RA_DG(self):
        """ calculates DG success based on running average
        """
        self.dg_running_av = hp.calc_running_average_list(self.dg_success, self.pm.running_AV)
        return self.dg_running_av
        
        
        
        

class CS():
    """ Conceptual Space containing percepts, lexicon and connection matrix
    """
    
    def __init__(self, parameters):
        self.pm = parameters
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
    
    
    def shift_cat(self, percept_tag, point):
        """ shifts provided percept towards provided point
        """
        coors = self.percepts[percept_tag]
        diff = [self.pm.learning_rate * x for x in map(operator.sub, coors, point)]
        self.percepts[percept_tag] = map(operator.add, coors, diff)        
        #meaning{a}(m(t),:) = closest + LEARNINGRATE * ( c(t,:) - closest );
                    

        
        
        
        