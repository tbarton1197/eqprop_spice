# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 10:29:15 2022

@author: tbart
"""

import components as co
import circuit
from layer import Layer, joinLayers
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.NgSpice.Shared import NgSpiceShared
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit import *

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)


ckt = circuit.Circuit("testCircuit", 4)
'''
R2 = el.R("R2", res = 50)
R1 = el.R("R1", res = 10)
V1 = el.V("V1", voltage = 10)
V2 = el.V("V2", voltage = 10)
N1 = el.neuron("X1")
N1.out = 4

ckt.addElements([R1, R2, V1, V2, N1])

ckt.connect(V1, R1);
ckt.connect(R1, R2)
ckt.connect(R2, V1)
ckt.connect(V2, R2)
ckt.connectN(R1, N1);
ckt.connectN(R2, N1)

'''



l1 = Layer('X1', 4, 1)
l2 = Layer('X2', 4, 1)
l3 = Layer('X3', 4, 1)
l4 = Layer('X4', 4, 1)
joinLayers(l1, l2)
joinLayers(l2, l3)
joinLayers(l3, l4)
ckt.addLayer(l1)
ckt.addLayer(l2)
ckt.addLayer(l3)
ckt.addLayer(l4)


numInputs = 2
Vins = []
vinVals = [1, 0]
for i in range(numInputs):
    Vins.append(co.V("vin_" + str(i), neg = 0, pos = l1.input_nets[i], voltage=vinVals[i]))
ckt.addElements(Vins)

ckt.printNetlist("layerTest")


ckt.printNetlist("test")
ckt.writeNetlist("test")
netlist = ckt.netlistToString("test")


parser = SpiceParser(source=netlist)
psCircuit = parser.build_circuit()
#psCircuit.include(spice_library['1N4148'])
print(psCircuit)

simulator = psCircuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

for node in analysis.nodes.values():
    print('Node {}: {:5.2f} V'.format(str(node), float(node))) # Fixme: format value + unit






