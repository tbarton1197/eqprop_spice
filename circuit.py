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
from PySpice.Spice.Parser import SpiceParser

import components as co

sp = " "
gnd = 0;

class Circuit():
    
    def __init__(self, circuitName, neuronGain):
        self.circuitName = circuitName
        self.nets = []
        self.nextNet = 1
        self.nets.append(gnd)
        self.neuronGain = neuronGain
        self.netlist = []
        
        
    
    def printNetlist(self, name):
        print(self.netlistToString(name))
        
    def writeNetlist(self, name):
        f = open(name + "_netlist.cir", "w")
        #f.write(".SUBCTK" + sp + name + sp + "1" + sp + "2" + "\n")
        f.write(".title testNetlist \n")
        
        f.write(self.writeNeuronSubcircuit())
        
        for x in self.netlist:
            if not isinstance(x, str):
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
        
       
    def writeNeuronSubcircuit(self):
        s0 = ".SUBCKT neuron in out \n"
        s1 = "E1 2 0 in 0 " + str(self.neuronGain) + " \n"
        s2 = '''V1 out 2 0
F1 in 0 V1 0.25
X1 in 0 1N4148
X2 0 in 1N4148

.ENDS
.SUBCKT 1N4148 1 2 

R1 1 2 5.827E+9 
D1 1 2 1N4148
*
.MODEL 1N4148 D 
+ IS = 4.352E-9 
+ N = 1.906 
+ BV = 110 
+ IBV = 0.0001 
+ RS = 0.6458 
+ CJO = 7.048E-13 
+ VJ = 0.869 
+ M = 0.03 
+ FC = 0.5 
+ TT = 3.48E-9 
.ENDS
'''
        return (s0 + s1 + s2) 
    
    def addElement(self, element):
        self.netlist.append(element)
        
    def addElements(self, elements):
        for i in elements:
            self.netlist.append(i)
        
    def connect(self, pos: co.twoTerm, neg: co.twoTerm):
        global nextNet
        
        if pos.pos == "" and neg.neg == "":
            pos.setPos(self.nextNet)
            neg.setNeg(self.nextNet)
            
        elif pos.pos != "" and neg.neg != "":
            raise Exception("Can't reconnect 2 object with existing connections") 
            
        elif pos.pos != "":
            neg.neg = pos.pos
        else:
            pos.pos = neg.neg
        
        self.nextNet += 1
        
    def connectN(self, pos: co.twoTerm, N: co.neuron):
        if(N.inputs == ""):
            pos.pos = self.nextNet;
            N.inputs = self.nextNet;
        else:
            pos.pos = N.inputs
            
    def addLayer(self, l):
        self.addElements(l.resistors)
        self.addElements(l.neurons)
       


def runSim(netlist):
    parser = SpiceParser(source=netlist)
    psCircuit = parser.build_circuit()
    #psCircuit.include(spice_library['1N4148'])
    #print(psCircuit)

    simulator = psCircuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()

    return analysis
    

        
    
    
    
    
    
    
    