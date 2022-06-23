# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:00:14 2022

@author: tbart
"""

sp = " "

class twoTerm ():
    def __init__(self, name, neg="", pos=""):
        global netlist
        self.name = name
        self.neg = neg
        self.pos = pos
    
    def getPos(self):
        return self.name + '_' + str(self.pos)
    
    def getNeg(self):
        return self.name + '_' + str(self.neg)
    
    def setPos(self, term):
        self.pos = term
        
    def setNeg(self, term):
        self.neg = term
        

#V neg defaults to ground
class V (twoTerm):
    def __init__(self, name, neg = 0, pos = "", voltage = 0):
        super().__init__(name, neg, pos)
        self.voltage = voltage
        
    def toNet(self):
        return self.name + sp + str(self.pos) + sp + str(self.neg) + sp + str(self.voltage)

    
class I(twoTerm):
    def __init__(self, name, neg = 0, pos = "", current = 0):
        super().__init__(name, neg, pos)
        self.current = current
        
    def toNet(self):
        return self.name + sp + str(self.pos) + sp + str(self.neg) + sp + str(self.current)

class R (twoTerm):
    def __init__(self,name, neg = "", pos = "", res = 0):
        super().__init__(name, neg, pos)
        self.res = res
        
    def toNet(self):
        return self.name + sp + str(self.pos) + sp + str(self.neg) + sp + str(self.res)

class neuron():
    def __init__(self, name, inputs = "", out = "", gain = 1):
        self.name = name
        self.out = out
        self.inputs = inputs
        self.gain = gain
        
    
        
    def toNet(self):
        return self.name + sp + str(self.inputs) + sp + str(self.out) + sp + "neuron"