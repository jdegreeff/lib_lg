
########################################################################
# lib_lg v0.1                                                          #
# agent.py                                                             #
# Joachim de Greeff                                                    #
#                                                                      #
# agents and Conceptual Space representation                           #
########################################################################


import operator
import pandas as pd
import lg, data
import help_functions as hp
import parameters as pm



class Agent():
    """ Basic agent structure consisting of a Conceptual Space, a lexicon and a connection matrix
        for implementation reasons the lexicon is not a separate structure, 
        but the header of the connection matrix
    """
    
    def __init__(self, name, learning=True):
        self.agent_name = name
        self.learning = learning        # specifies if the agent is learning; typically a teaching agent will not learn
        
        self.cs = CS()                  # CS containing percepts
        self.matrix = pd.DataFrame()    # matrix containing connection strength between words and percepts
        
        # keeping track of LG performance
        self.dg_success = []
        self.dg_running_av = []
        self.dg_n_percepts = []
        
        
    def load_knowledge(self):
        """ loads predefined knowledge, typically done by teaching agent
        """
        if pm.domain == "rgb":
            for i in data.basic_colour_data.keys():
                tag = "percept" + str(len(self.cs.percepts.keys()))
                self.cs.percepts[tag] = data.basic_colour_data[i]
                self.update_matrix(i, tag)
            self.matrix = self.matrix.fillna(0) # set NaN values to 0
        
        
    def calculate_RA_DG(self):
        """ calculates DG success based on running average
        """
        latest_RA = hp.calc_running_average_list(self.dg_success, pm.running_AV)
        self.dg_running_av.append(latest_RA)
        return self.dg_running_av[-1]
    
    
    def get_word(self, percept_tag):
        """ returns word with highest connection based on provided percept_tag
            if percept_tag is novel, a new word + connection is created
        """
        if percept_tag in self.matrix.index:
            word = self.matrix.loc[percept_tag].idxmax()
        else:
            word = self.create_word(percept_tag)
        return word

        
    def create_word(self, percept_tag):
        """ create new word and connect to provided percept_tag with default connection
        """
        new_word = hp.generateRandomWord(self.lexicon, 6)
        self.update_matrix(new_word, percept_tag)
        self.matrix = self.matrix.fillna(0) # set NaN values to 0
        return new_word
        
        
    def update_matrix(self, word, percept_tag, value=0.5):
        """ updates matrix for provided word and concept tag with the optional value
        """
        self.matrix.loc[percept_tag, word] = value
        
        
    def answer_gg(self, context, word):
        """ make a guess regarding topic based on provided context and word
        """
        if word in self.matrix.columns:
            percept_tag = self.matrix[word].idxmax()
            distances = [hp.calc_euclidean_distance(i, self.percepts[percept_tag]) for i in context]
            return distances.index(min(distances))
        else:
            return "word unknown"
        
        
        

class CS():
    """ Conceptual Space containing percepts, lexicon and connection matrix
    """
    
    def __init__(self):
        self.percepts = {}
        
        
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
                    

        
        
        
        