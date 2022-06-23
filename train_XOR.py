import numpy as np
import components as co
import circuit
from layer import Layer, joinLayers
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.NgSpice.Shared import NgSpiceShared
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
import random as rand

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit import *
import time

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)





numInputs = 2
testMode = False


beta = 0.001
np.random.seed(1)
resistances = np.ones([4,2])*np.ceil(np.random.random([4,2])*10)*100

# resistances = [[10, 16, 12, 20],[9, 177, 83, 8]]
# resistances = np.transpose(np.array(resistances))

numEpochs = 20

for i in range(numEpochs):
    print("Epoch # " + str(i))
    
    Vins = []
    
    vinVals = [rand.randint(0,1),rand.randint(0,1)]
    
    for v in vinVals:
        if v == 0:
            v = -2
        if v == 1:
            v = 2
    
    vinVals = [2, 2]
    exp_out = int(bool(vinVals[0]) != bool(vinVals[1]))
    
    exp_out = 0
    print("Vin: " + str(vinVals))
    print("exp out: " + str(exp_out))
    ckt = circuit.Circuit("testCircuit", 4)
    
    l1 = Layer('X1', 2, 1, resistances[:,0])
    l2 = Layer('X2', 2, 1, resistances[:,1], is_output = True)
    joinLayers(l1, l2)
    ckt.addLayer(l1)
    ckt.addLayer(l2)

   # add a bias neuron
    Vbias = co.V("vbias", neg = 0, pos = "vbin1", voltage=1)
    Rb1 = co.R("rb1", neg = "vbin1", pos = "X1_Nin_0", res = 80000)
    Rb2 = co.R("rb2", neg = "vbin1", pos = "X1_Nin_1", res = 17)

    ckt.addElements([Vbias, Rb1, Rb2])

    for i in range(numInputs):
        Vins.append(co.V("vin_" + str(i), neg = 0, pos = l1.input_nets[i], voltage=vinVals[i]))
    ckt.addElements(Vins)

    ckt.writeNetlist("test")


    netlist = ckt.netlistToString("test")
    
    
    analysis = circuit.runSim(netlist)
    
    outputs = []
    output_names = []
    
    for node in analysis.nodes.values():
        if testMode:
            print('Node {}: {:5.2f} V'.format(str(node), float(node)))
        
        if "output_net" in str(node):
            outputs.append(float(node))
            output_names.append(str(node))
            
    dv1 = np.power(l1.getDeltaV(analysis), 2)
    dv2 = np.power(l2.getDeltaV(analysis), 2)
    
    y_hat = outputs[1] - outputs[0]
    loss = (exp_out - y_hat)**2
    Ikp = beta * (exp_out - outputs[1] + outputs[0])
    Ikn = beta * (exp_out - outputs[1] - outputs[0])
    print("actual out: " + str(y_hat))
    print("loss: " + str(loss))
    
    I0 = co.I("I0", neg=0, pos = output_names[0], current=Ikn)
    I1 = co.I("I1", neg=0, pos = output_names[1], current=Ikp)
    ckt.addElements([I0, I1])
    
    print("\n\n")
    #ckt.printNetlist("test")
    #print("\n\n")
    
    netlist = ckt.netlistToString("test")
    analysis = circuit.runSim(netlist)
    
    post_outputs = []
    
    for node in analysis.nodes.values():
        if testMode:
            print('Node {}: {:5.2f} V'.format(str(node), float(node)))
        
        if "output_net" in str(node):
            post_outputs.append(float(node))
            
    dif = np.subtract(post_outputs, outputs)
    
    #calculate voltage drops
    dv1_beta = np.power(l1.getDeltaV(analysis), 2)
    dv2_beta = np.power(l2.getDeltaV(analysis), 2)
    
    alpha = 0.001
    
    conductances = np.divide(1, resistances)
    
    conductances[:,0] = conductances[:,0] - (alpha / beta) * (np.subtract(dv1_beta, dv1))
    conductances[:,1] = conductances[:,1] - (alpha / beta) * (np.subtract(dv2_beta, dv2))
    
    resistances = np.divide(1, conductances)
    
    # for j in range(4):
    #     for k in range(2):
    #         if resistances[j][k] < 5:
    #             resistances[j][k] = 5
    
    #l1.updateResistances(resistancespost[:,0])
    #l2.updateResistances(resistancespost[:,1])
    #time.sleep(1)



#do inference





