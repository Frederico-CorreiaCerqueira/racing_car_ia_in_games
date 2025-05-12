class DTAgent(object):
    
    def __init__(self,name,dt):
        self.name=name
        self.sensors=None
        self.dt=dt
    
    def update_sensors(self):
        raise NotImplementedError
    
    def decision(self):
        action=(self.dt).decide(self.sensors)
        eval('self.'+action+'()')