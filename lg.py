
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

        agent.calculate_RA_DG()
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
        
        # if success, increase connections and shift learner category towards topic
        if a2_gg_response[0] == topic_index:
            agent1.update_matrix(a1_word, a1_percept, pm.delta)
            agent2.update_matrix(a1_word, a2_gg_response[1], pm.delta)
            agent2.cs.shift_percept(a2_gg_response[1], context[topic_index])
            agent1.gg_success.append(1)
            agent2.gg_success.append(1)
            
        # if agent2 does not know agen1 word, learn this
        elif a2_gg_response == "word unknown":
            a2_percept = self.discrimination_game(agent2, context, topic_index)
            agent2.add_word(a2_percept, a1_word)
            agent1.gg_success.append(0)
            agent2.gg_success.append(0)
        
        # agent2 knows word, but points to wrong topic, decrease connection and play DG
        else:
            if pm.current_game > 500:
                pass
            agent2.update_matrix(a1_word, a2_gg_response[1], -pm.delta)
            a2_percept = self.discrimination_game(agent2, context, topic_index)
            agent2.add_word(a2_percept, a1_word)
            agent1.gg_success.append(0)
            agent2.gg_success.append(0)
        
        agent2.calculate_RA_GG()
        pm.current_game += 1



    def run_discrimination_game(self):
        """ run a series of discrimination games
        """
        print "starting DG"
        
        all_results, all_n_percepts = [], []
        
        for i in range(pm.n_replicas):
            
            agent1 = agent.Agent("agent1")
            for j in self.td:
                self.discrimination_game(agent1, j, random.randint(0, pm.context_size-1))
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
        
        all_results = []
        
        for i in range(pm.n_replicas):
        
            agent1 = agent.Agent("agent1", learning=False)
            agent1.load_knowledge() # as agent1 is the teacher, it needs some predefined knowledge
            
            agent2= agent.Agent("agent2")
            
            for x, j in enumerate(self.td):
                self.guessing_game(agent1, agent2, j, random.randint(0, pm.context_size-1))
                if x == 500:
                    pass
            
            print "end replica " + str(i)
            all_results.append(agent2.gg_running_av)
            
        av_results = hp.calc_average(all_results)
        output.plot_DG(av_results)
        
        agent2.matrix.to_csv("output.csv")
        import csv
        w = csv.writer(open("output2.csv", "w"))
        for key, val in agent2.cs.percepts.items():
            w.writerow([key, val])

        
        
        
        
    def population_LG(self):
        """ language game with a population of agents
        """
    


