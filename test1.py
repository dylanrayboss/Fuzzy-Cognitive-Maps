# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:16:15 2016

@author: Eric
"""

#from FCM import FCM
#from FCM import simulation
import math
import FCM

def transFunct(x):
    return (1/(1+math.exp(-x)))

test_fcm = FCM.FCM()

test_fcm.add_concept("Tank1")
test_fcm.add_concept("Tank2")
test_fcm.add_concept("Valve1")
test_fcm.add_concept("Valve2")
test_fcm.add_concept("Valve3")
test_fcm.add_concept("Heat element")
test_fcm.add_concept("Therm_tank1")
test_fcm.add_concept("Therm_tank2")

test_fcm.set_value("Tank1",.2)
test_fcm.set_value("Tank2",.01)

test_fcm.set_value("Valve1",.55)
test_fcm.set_value("Valve2",.58)
test_fcm.set_value("Valve3",.0)

test_fcm.set_value("Heat element",.2)
test_fcm.set_value("Therm_tank1",.1)
test_fcm.set_value("Therm_tank2",.05)

test_fcm.add_edge("Tank1","Valve1",.21)
test_fcm.add_edge("Tank1","Valve2",.38)
test_fcm.add_edge("Tank2","Valve2",.7)
test_fcm.add_edge("Tank2","Valve3",.6)
test_fcm.add_edge("Valve1","Tank1",.76)
test_fcm.add_edge("Valve2","Tank1",-.6)
test_fcm.add_edge("Valve2","Tank2",.8)
test_fcm.add_edge("Valve2","Therm_tank2",.09)
test_fcm.add_edge("Valve3","Tank2",-.42)
test_fcm.add_edge("Heat element","Therm_tank1",.6)
test_fcm.add_edge("Therm_tank1","Heat element",.53)
test_fcm.add_edge("Therm_tank1","Valve1",.4)
test_fcm.add_edge("Therm_tank2","Valve2",.3)

test_fcm.draw()

sim_test = FCM.simulation(test_fcm)

sim_test.steps(10)

sim_test.stabilize("Valve3", .001)

sim_test.changeTransferFunction(transFunct)

testList = sim_test.run()

print "\n\n\n\n"
print testList