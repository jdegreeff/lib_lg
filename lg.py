
# Top level language game

import parameters





class LG():
    """ generic Language Game
    """
    def __init__(self, type):
        self.type = type
        self.agents = {}
        self.parameters = parameters.Parameters()
        
        
class two_agents_LG(LG):
    """ language game with two agents (typically teacher and learner)
    """
    def __init__(self):
        LG.__init__(self, "two_agents_LG")
        
        
class population_LG(LG):
    """ language game with a population of agents
    """
    def __init__(self):
        LG.__init__(self, "population_LG")


class Agent():
    """ Agent
    """
    
    def __init__(self, name="agent"):
        self.agent_name = name