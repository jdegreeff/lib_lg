
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
        self.gg_success = []
        self.gg_running_av = []
        
        
    def load_knowledge(self):
        """ loads predefined knowledge, typically done by teaching agent
        """
        if pm.domain == "rgb":
            for i in data.basic_colour_data.keys():
                tag = "percept" + str(len(self.cs.percepts.keys()))
                self.cs.percepts[tag] = data.basic_colour_data[i]
                self.matrix.loc[tag, i] = 0.5
            self.matrix = self.matrix.fillna(0) # set NaN values to 0
        
        
    def calculate_RA_DG(self):
        """ calculates DG success based on running average
        """
        latest_RA = hp.calc_running_average_list(self.dg_success, pm.running_AV)
        self.dg_running_av.append(latest_RA)
        
        
    def calculate_RA_GG(self):
        """ calculates GG success based on running average
        """
        latest_RA = hp.calc_running_average_list(self.gg_success, pm.running_AV)
        self.gg_running_av.append(latest_RA)
    
    
    def get_word(self, percept_tag):
        """ returns word with highest connection based on provided percept_tag
            if percept_tag is novel, a new word + connection is created
        """
        if percept_tag in self.matrix.index:
            word = self.matrix.loc[percept_tag].idxmax()
        else:
            word = self.add_word(percept_tag)
        return word

        
    def add_word(self, percept_tag, new_word=None):
        """ adds a provided percept_tag and optional word to connection matrix with default connection
            if no word is provided, a new word is created
        """
        if not new_word:
            new_word = hp.generateRandomWord(self.lexicon, 6)
        self.matrix.loc[percept_tag, new_word] = 0.5
        self.matrix = self.matrix.fillna(0) # set NaN values to 0
        return new_word
        
        
    def update_matrix(self, word, percept_tag, value):
        """ updates matrix for provided word and concept tag with value
        """
        connection = self.matrix.loc[percept_tag, word]
        self.matrix.loc[percept_tag, word] = connection + value
        if self.matrix.loc[percept_tag, word] > 1.0:
            self.matrix.loc[percept_tag, word] = 1.0
        if self.matrix.loc[percept_tag, word] < 0.0:
            self.matrix.loc[percept_tag, word] = 0.0
        
        
    def answer_gg(self, context, word):
        """ make a guess regarding topic based on provided context and word
        """
        if word in self.matrix.columns:
            percept_tag = self.matrix[word].idxmax()
            distances = [hp.calc_euclidean_distance(i, self.cs.percepts[percept_tag]) for i in context]
            return [distances.index(min(distances)), percept_tag]
        else:
            return "word unknown"
        



class CS():
    """ Conceptual Space containing percepts
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
        self.percepts[percept_tag] = [ 1.0 if i > 1.0 else i for i in self.percepts[percept_tag] ]
        self.percepts[percept_tag] = [ 0.0 if i < 0.0 else i for i in self.percepts[percept_tag] ]
        #meaning{a}(m(t),:) = closest + LEARNINGRATE * ( c(t,:) - closest );
                    

        
        
        
        