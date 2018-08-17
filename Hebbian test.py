# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 22:51:23 2016

@author: Eric
"""
import FCM
from math import exp
#declare the fcm for test
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
#make needed arguments for learning
hebStableDict = {}
hebStableDict["Valve3"] = .001
hebStableDict["Valve1"] = .001
hebStableDict["Valve2"] = .001

valve3Tup = (.5,.65)
valve2Tup = (.65,.7)
restraints = {}
restraints['Valve3'] = valve3Tup
restraints['Valve2'] = valve2Tup

print "The result of the hebbian learning was the following edge Matrix:"
print FCM.Hebbian.hebbian_learning(test_fcm,restraints, hebStableDict,lambda x: 1/(1+exp(-x)),.2,100)