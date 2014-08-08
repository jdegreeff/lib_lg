
import numpy as np
import help_functions as hp



class Agent():
    """ Agent
    """
    
    def __init__(self, name, parameters):
        self.agent_name = name
        self.dg_success = []
        self.cs = CS(parameters.n_dimensions)
        
        
    def match_CS_to_context(self, context):
        matches = []
        for i in context:
            matches.append(self.cs.get_best_match(i))
        return matches


class CS():
    """ Conceptual Space containing percepts, lexicon and connection matrix
    """
    
    def __init__(self, n_dimensions):
        self.n_dimensions = n_dimensions
        self.percepts = {}
        self.lexicon = []
        #self.matrix = np.array()
        
        
    def get_best_match(self, point):
        """ returns best matching percept for given point
        """
        distance = 9999999999999999
        best_match = ""
        for i in self.percepts.keys():
            dist = hp.calc_euclidean_distance(point, self.percepts[i])
            if dist < distance:
                distance = dist
                best_match = i
        return best_match
        
        
        
        