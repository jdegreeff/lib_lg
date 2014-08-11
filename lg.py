
# Top level language game

import random
import agent
import help_functions as hp



class LG():
    """ generic Language Game
    """
    def __init__(self, gametype, parameters):
        self.gametype = gametype
        self.pm = parameters
        self.td = self.generate_training_data()
        
        
    def generate_training_data(self):
        dim = self.pm.n_dimensions
        con = self.pm.context_size
        inter = self.pm.n_interactions
        return [ hp.generate_context(dim, con, self.pm.object_distance, self.pm.max_retries) for _ in xrange(inter)]
    

        
    def run_discrimination_game(self):
        """ run a DG
        """
        print "starting DG"
        agent1 = agent.Agent("agent1", self.pm)
        for x, i in enumerate(self.td):
            self.discrimination_game(agent1, i, random.randint(0, self.pm.context_size-1))
            print "DG " + str(x)
        print "percepts: ", len(agent1.cs.percepts)
        print "success: ", agent1.dg_running_av
        #print "success: ", sum(agent1.dg_success)/(1.0*self.pm.n_interactions)
            
        
        
    def discrimination_game(self, agent, context, topic_index):
        """ Discrimination Game played by one agent
        """
        
        if len(agent.cs.percepts) == 0:
            agent.cs.percepts["percept0"] = context[topic_index]
            agent.dg_success.append(0)
            return "percept0"
        
        else:
            for i in context:
                if i == "c":
                    break
            best_matches = [ agent.cs.get_best_match(i) for i in context ]
            
            # DG succeeds
            if best_matches.count(best_matches[topic_index]) == 1:
                print "success"
                agent.dg_success.append(1)
                return best_matches[topic_index]
            
            # DG fails
            else:
                print "fail"
                agent.dg_success.append(0)
                
                # shift cat
                if (agent.calculate_RA_DG() > self.pm.adapt):
                    agent.cs.shift_cat(best_matches[topic_index], context[topic_index])
                    return best_matches[topic_index]
                    
                # create new cat
                else:
                    tag = "percept" + str(len(agent.cs.percepts.keys()))
                    agent.cs.percepts[tag] = context[topic_index]
                    return tag



    def two_agents_LG(self):
        """ language game with two agents (typically teacher and learner)
        """
        
        
    def population_LG(self):
        """ language game with a population of agents
        """
    


