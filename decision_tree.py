""" An object oriented implementation of a decision tree
No __init__ method in the most general class
"""

class Node(object):
    """ Abstract Tree Root implementation
    """

    def decide(self, info):
        raise NotImplementedError
    

# Behavior or action nodes
# which also "decide" but the decesion method return que também têm decide mas em que o decide devolve o método run
class Action(Node):
    """ nome da acção
    """
    def __init__(self,name):
        self.name=name


    def decide(self, _):
        return self.name
    

# Há nos de decisão 
class Decision(Node):
    """ Abstract interior node implementation
    """

    def __init__(self, attr, daughters):
        self._attribute = attr
        self._daughter_nodes = daughters

    def decide(self, info):
        return self.getBranch(info).decide(info)
    
    def value(self,info):
        return info[self._attribute]


    def getBranch(self,info):
        return self._daughter_nodes[self.value(info)]
    
    
class Boolean(Decision):
    """ Abstract boolean decision node implementation
    """

    def __init__(self, attr,yesNode,noNode):
        super(Boolean, self).__init__(attr,{True: yesNode, False: noNode})