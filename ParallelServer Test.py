import FCM
from FCM import simulation
import math, time

def transFunct(x):
    return 1/(1+math.exp(-x))

#declare the fcm for test
fcm1 = FCM.FCM()

fcm1.add_concept("Tank1")
fcm1.add_concept("Tank2")
fcm1.add_concept("Valve1")
fcm1.add_concept("Valve2")
fcm1.add_concept("Valve3")
fcm1.add_concept("Heat element")
fcm1.add_concept("Therm_tank1")
fcm1.add_concept("Therm_tank2")

fcm1.set_value("Tank1",.2)
fcm1.set_value("Tank2",.01)

fcm1.set_value("Valve1",.55)
fcm1.set_value("Valve2",.58)
fcm1.set_value("Valve3",.0)

fcm1.set_value("Heat element",.2)
fcm1.set_value("Therm_tank1",.1)
fcm1.set_value("Therm_tank2",.05)

fcm1.add_edge("Tank1","Valve1",.21)
fcm1.add_edge("Tank1","Valve2",.38)
fcm1.add_edge("Tank2","Valve2",.7)
fcm1.add_edge("Tank2","Valve3",.6)
fcm1.add_edge("Valve1","Tank1",.76)
fcm1.add_edge("Valve2","Tank1",-.6)
fcm1.add_edge("Valve2","Tank2",.8)
fcm1.add_edge("Valve2","Therm_tank2",.09)
fcm1.add_edge("Valve3","Tank2",-.42)
fcm1.add_edge("Heat element","Therm_tank1",.6)
fcm1.add_edge("Therm_tank1","Heat element",.53)
fcm1.add_edge("Therm_tank1","Valve1",.4)
fcm1.add_edge("Therm_tank2","Valve2",.3)
#make needed arguments for learning
stabilizers1 = {}
stabilizers1["Valve3"] = .001
stabilizers1["Valve1"] = .001
stabilizers1["Valve2"] = .001

fcm2 = FCM.FCM()

fcm2.add_concept("Wetland")
fcm2.add_concept("Fish")
fcm2.add_concept("Pollution")
fcm2.add_concept("Livelihood")
fcm2.add_concept("Laws")

fcm2.add_edge("Wetland","Fish",1.0)
fcm2.add_edge("Wetland","Pollution",-.1)
fcm2.add_edge("Wetland","Livelihood",.8)
fcm2.add_edge("Fish","Livelihood",1.0)
fcm2.add_edge("Pollution","Wetland",-.2)
fcm2.add_edge("Pollution","Fish",-1.0)
fcm2.add_edge("Pollution","Livelihood",-.2)
fcm2.add_edge("Laws","Wetland",.2)
fcm2.add_edge("Laws","Fish",.5)
fcm2.add_edge("Laws","Pollution",-.5)
fcm2.add_edge("Laws","Livelihood",-.2)

fcm2.set_value("Wetland",1.0)
fcm2.set_value("Fish",1.0)
fcm2.set_value("Pollution",1.0)
fcm2.set_value("Livelihood",1.0)
fcm2.set_value("Laws",1.0)

stabilizers2 = {}
stabilizers2["Fish"] = .001
stabilizers2["Livelihood"] = .001

FCMs = {}
FCMs[fcm1] = stabilizers1
FCMs[fcm2] = stabilizers2

print "The result of simulating the two test FCMs on a server was:"
FCM.ParallelServer.parallelS(FCMs)

print "\n\nThe result of simulating the two test FCMs without parallelization was:"

start_time = time.time()

sim1 = simulation(fcm1)

sim1.steps(10000)

sim1.changeTransferFunction(transFunct)

sim1.stabilize("Valve3", .001)
sim1.stabilize("Valve1", .001)
sim1.stabilize("Valve2", .001)

sim1.run(.1)

sim2 = simulation(fcm2)

sim2.steps(10000)

sim2.changeTransferFunction(transFunct)

sim2.stabilize("Fish",.001)
sim2.stabilize("Livelihood",.001)

sim2.run() 

print "\nTime elapsed: ", time.time() - start_time, "s"

print "\n\nThe result of using the transfer function on a server was:"
FCM.ParallelServer.parallelT(10)