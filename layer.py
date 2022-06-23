# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:36:12 2022

@author: tbart
"""

import components as co
import numpy as np
import random

class Layer:
    
    
    def __init__(self, name, numNeurons, spread, resistances, is_output = False):
        self.name = name
        self.numNeurons = numNeurons
        self.spread = spread
        self.input_nets = []
        self.output_nets = []
        self.resistors = []
        self.neurons = []
        self.is_output = is_output
        self.resistances = resistances
        
        
        for i in range(numNeurons):
            self.input_nets.append(self.name + "_in_" + str(i))
            self.output_nets.append(self.name + "_out_" + str(i))
            if is_output == False:
                self.neurons.append(co.neuron(self.name + "_neuron_" + str(i), inputs = self.name + "_Nin_" + str(i), out = self.output_nets[i]))
            else:
                self.neurons.append("output_net_" + str(i))
                
        resCounter = 0                
                
        for i in range(numNeurons):   
            
            rtop = i + spread
            rbot = i - spread
            if rtop > numNeurons - 1:
                rtop = numNeurons - 1
            if rbot < 0:
                rbot = 0
                
            for r in range(rbot, rtop+1):
                if not self.is_output:
                    output_net = self.neurons[r].inputs
                else:
                    output_net = self.neurons[r]
                R = co.R("r_" + self.input_nets[i] + str(r), res = self.resistances[resCounter], neg = self.input_nets[i], pos=output_net)
                resCounter += 1
                self.resistors.append(R)
            
        

    
    def toNet(self):
        
        ns = ""
        for r in self.resistors:
            ns += r.toNet()
            ns += "\n"
        
        for n in self.neurons:
            ns += n.toNet();
            ns += "\n"
    
        return ns
    
    def getDeltaV(self, analysis):
        
        vdrop = []
        for r in self.resistors:
            v_pos = float(analysis.nodes[r.pos.lower()])
            v_neg = float(analysis.nodes[r.neg.lower()])
            
            vdrop.append( (v_neg) - (v_pos) )
            
        return vdrop
    
    def updateResistances(self, newR):
        
        for r in range(len(self.resistors)):
            self.resistors[r].res = newR[r]
            
            
            
        
    
    
def joinLayers(l1, l2):
    for i in range(len(l2.output_nets)):
        l1.output_nets[i] = l2.input_nets[i]
        
    for n in range(len(l1.neurons)):
        l1.neurons[n].out = l1.output_nets[n]
    
        

    
    
    
    
    
    