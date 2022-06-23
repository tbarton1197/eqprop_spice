# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 10:21:12 2022

@author: tbart
"""

import numpy as np
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

from PySpice.Spice.Netlist import Circuit, SubCircuit, SubCircuitFactory
from PySpice.Unit import *
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary

sp = " "
gnd = 0;

class Circuit():
    
    def __init__(self, circuitName):
        self.circuitName = circuitName
        self.nets = []
        self.nextNet = 1
        self.nets.append(gnd)
        
        self.netlist = []
        
        
    
    def printNetlist(self, name):
        print(self.netlistToString(name))
        
    def writeNetlist(self, name):
        f = open(name + "_netlist.cir", "w")
        #f.write(".SUBCTK" + sp + name + sp + "1" + sp + "2" + "\n")
        f.write(".title testNetlist \n")
        
        f.write(self.writeNeuronSubcircuit())
        
        for x in self.netlist:
            f.write(x.toNet() + "\n")
        #f.write(".backanno" + "\n")
        f.write(".op" + "\n")
        f.write(".end" + "\n")
        f.close()
        
    def netlistToString(self, name):
        self.writeNetlist(name)
        f = open(name + "_netlist.cir", "r")
        netlist = f.read()
        f.close()
        return netlist;
        
       
    def writeNeuronSubcircuit():
        s0 = ".SUBCKT neuron in out \n"
        #s1 = "D1 in 0 1N4148 \n"
        #s2 = "D2 0 in 1N4148  \n"
        s3 = "E1 out 0 in 0 4 \n"
        #s4 = ".model D D  \n"
        #s5 = ".lib C:/Users/tbart/Documents/LTspiceXVII/lib/cmp/standard.dio \n"
        s6 = ".ends \n"
        return (s0 + s3 + s6) 
    
    def addElement(self, element):
        self.netlist.append(element)
        
    def connect(self, pos: elements.twoTerm, neg: elements.twoTerm):
        global nextNet
        
        if pos.pos == "" and neg.neg == "":
            pos.setPos(nextNet)
            neg.setNeg(nextNet)
            
        elif pos.pos != "" and neg.neg != "":
            raise Exception("Can't reconnect 2 object with existing connections") 
            
        elif pos.pos != "":
            neg.neg = pos.pos
        else:
            pos.pos = neg.neg
        
        nextNet += 1
        
    def connectN(self, pos: elements.twoTerm, N: elements.neuron):
        if(N.inputs == ""):
            pos.pos = nextNet;
            N.inputs = nextNet;
        else:
            pos.pos = N.inputs
       


    

        
    
    
    
    
    
    
    