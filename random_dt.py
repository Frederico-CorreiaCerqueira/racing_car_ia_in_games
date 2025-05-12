import random

from decision_tree import Decision


class RandomDecision(Decision):
    """ A Random Decision--- uniform 
    """
    def __init__(self,daughters):
        #super(Decision, self).__init__(attr,daughters)
        self._daughter_nodes=daughters
        
    def decide(self,info):
        d=random.choice(self._daughter_nodes)
        return d.decide(info)
    

class RandomDecisionPeriod(Decision):
    """ A Random Decision--- uniform -during a certain number of ticks or frames or calls 
    """
    def __init__(self,daughters,lim):
        #super(Decision, self).__init__(attr,daughters)
        self._daughter_nodes=daughters
        self.lim=lim
        self.ticks=lim
        self.current_decision=random.choice(self._daughter_nodes)
        
    def decide(self,info):
        if  self.ticks <= 0:
            new_dec=random.choice(self._daughter_nodes)
            while new_dec==self.current_decision:
                new_dec=random.choice(self._daughter_nodes)
            self.current_decision=new_dec
            self.ticks=self.lim-1
        self.ticks-=1
        return self.current_decision.decide(info)