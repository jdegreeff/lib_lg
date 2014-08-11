

class Parameters():
    """ parameter class
    """
    def __init__(self):
        
        # language games
        self.n_interactions = 1000
        self.n_replicas = 10
        self.adapt = 0.9
        self.learning_rate = 0.15           # Rate at which meanings should be shifted
        self.running_AV = 20                # Number of games over which running avg is taken
        
        # learning data
        self.n_dimensions = 3
        self.context_size = 3
        self.max_retries = 500              # maximal times for trying to generate a context with minimum distance between objects
        self.object_distance = 0.4;         # Minimum distance between objects in a context (considered along a line, corrected for higher dimensions)