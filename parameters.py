
########################################################################
# lib_lg v0.1                                                          #
# parameters.py                                                        #
# Joachim de Greeff                                                    #
#                                                                      #
# single class containing all parameters used                          #
########################################################################


# language games
n_interactions = 1000
n_replicas = 10
adapt = 0.9
learning_rate = 0.15           # Rate at which meanings should be shifted
running_AV = 20                # Number of games over which running avg is taken

# learning data
domain = "rgb"                 # domain used in LG
n_dimensions = 3
context_size = 3
max_retries = 500              # maximal times for trying to generate a context with minimum distance between objects
object_distance = 0.4;         # Minimum distance between objects in a context (considered along a line, corrected for higher dimensions)