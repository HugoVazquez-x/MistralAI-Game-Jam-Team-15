def increase_angagement_from_anger(anger, 
                             lower_bound=3,
                             upper_bound=10):
    """
    converts the average anger level into
    a variation in terms of viewers
    """
    return lower_bound + (anger * (upper_bound - lower_bound) / upper_bound)

class Engagement():
    def __init__(self,engagement_0=0):
        
        self.engagement=engagement_0
    
    def steer_engagement(self, trump_anger, kamala_anger):
        """
        steers the audience depending on the anger level
        of one of the contenders

        if the audience is steered down, it is for kamala
        if the audience is steered up, it is for trump
        """

        steered_towards_kamala=increase_angagement_from_anger(trump_anger)
        steered_towards_trump=increase_angagement_from_anger(kamala_anger)

        new_engagement=self.engagement - steered_towards_kamala + steered_towards_trump
        self.engagement=new_engagement
        
        return self.engagement

