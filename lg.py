
########################################################################
# lib_lg v0.1                                                          #
# agent.py                                                             #
# Joachim de Greeff                                                    #
#                                                                      #
# Top level language games                                             #
# The following language games are implemented:                        #
# - Discrimination Game (DG): game played with a single agent          #
# - Two-agents language game: game played between teacher and learner  #
# - Population language game: game played with population of agents    #
#                                                                      #
########################################################################

import random
import agent, output
import help_functions as hp
import parameters as pm



class LG():
    """ generic Language Game
    """
    def __init__(self, gametype):
        self.gametype = gametype
        self.td = self.generate_training_data()
        
        
    def generate_training_data(self):
        dim = pm.n_dimensions
        con = pm.context_size
        inter = pm.n_interactions
        return [ hp.generate_context(dim, con, pm.object_distance, pm.max_retries) for _ in xrange(inter)]
    

   
    def discrimination_game(self, agent, context, topic_index):
        """ Discrimination Game played by one agent
        """
        
        return_tag = ""
        
        if len(agent.cs.percepts) == 0:
            agent.cs.percepts["percept0"] = context[topic_index]
            agent.dg_success.append(0)
            return_tag = "percept0"
        
        else:
            best_matches = [ agent.cs.get_best_match(i) for i in context ]
            
            # DG succeeds
            if best_matches.count(best_matches[topic_index]) == 1:
                agent.dg_success.append(1)
                return_tag = best_matches[topic_index]
            
            # DG fails
            else:
                agent.dg_success.append(0)
                
                # shift cat
                if (agent.dg_running_av[-1] > pm.adapt):
                    agent.cs.shift_percept(best_matches[topic_index], context[topic_index])
                    return_tag = best_matches[topic_index]
                    
                # create new cat
                else:
                    tag = "percept" + str(len(agent.cs.percepts.keys()))
                    agent.cs.percepts[tag] = context[topic_index]
                    return_tag = tag

        return return_tag
    
    
    
    def guessing_game(self, agent1, agent2, context, topic_index):
        """ Guessing Game played by two agents
        """
        
        # agent1 perceives context and finds word
        if agent1.learning:
            a1_percept = self.discrimination_game(agent1, context, topic_index)
        else:
            a1_percept = agent1.cs.get_best_match(context[topic_index])
        a1_word = agent1.get_word(a1_percept)
        
        # agent2 makes guess based on agent1 word
        a2_gg_response = agent2.answer_gg(context, a1_word)
        
        
        if a2_gg_response == topic_index:
            print "success"
            
        else:
            print "fail"
        



    def run_discrimination_game(self):
        """ run a series of discrimination games
        """
        print "starting DG"
        
        all_results, all_n_percepts = [], []
        
        for i in range(pm.n_replicas):
            
            agent1 = agent.Agent("agent1")
            for j in self.td:
                self.discrimination_game(agent1, j, random.randint(0, pm.context_size-1))
                agent1.calculate_RA_DG()
                agent1.dg_n_percepts.append(len(agent1.cs.percepts))
                
            print "percepts: ", len(agent1.cs.percepts)
            print "success at end of replica " + str(i) + ": " + str(agent1.dg_running_av[-1])
            
            all_results.append(agent1.dg_running_av)
            all_n_percepts.append(agent1.dg_n_percepts)
        
        av_results = hp.calc_average(all_results)
        av_percepts = hp.calc_average(all_n_percepts)
        output.plot_DG(av_results, av_percepts)



    def two_agents_LG(self):
        """ language game with two agents (typically teacher and learner)
        """
        
        for i in range(pm.n_replicas):
        
            agent1 = agent.Agent("agent1", learning=False)
            agent1.load_knowledge() # as agent1 is the teacher, it needs some predefined knowledge
            
            agent2= agent.Agent("agent2")
            
            for j in self.td:
                self.guessing_game(agent1, agent2, j, random.randint(0, pm.context_size-1))
            
            print "end replica " + str(i)

        
        
        
        
    def population_LG(self):
        """ language game with a population of agents
        """
    


