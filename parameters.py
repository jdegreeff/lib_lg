

class Parameters():
    """ parameter class
    """
    def __init__(self):
        
        # language games
        self.n_interactions = 100
        self.n_replicas = 10
        self.adapt = 0.9
        
        # learning data
        self.n_dimensions = 3
        self.context_size = 4