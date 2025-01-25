class Engagement():
    def __init__(self):
        
        self.current_value = 0
        self.timestamp = 0
    
    def update(self, candidate_1_anger : float, candidate_2_anger: float):
        delta_anger = candidate_1_anger - candidate_2_anger
        self.current_value = self.current_value - (delta_anger)
        self.current_value = max(-1, min(self.current_value, 1))
        self.timestamp += 1

