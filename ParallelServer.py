import time, pp, math
from Simulation import simulation

'''
    parallelizeS
    Parameters:
    fcm: An fcm already created
    stabilizers: Concepts to stabilize on and their stabilization threshold.
    Returns: The new concept values acquired from running simulation.
    Description: Creates a parallelized simulation process to be ran on the server.
'''

def parallelizeS(fcm, stabilizers):
    sim = simulation(fcm)
    
    for key in stabilizers:
        sim.stabilize(key,stabilizers[key])
    
    #simulate until 10000 steps or stability reached
    sim.steps(10000)
    sim.changeTransferFunction(lambda x: 1/(1+math.exp(-x)))
    values = sim.run()
    return values
    
'''
    parallelizeT
    Parameters: None.
    Returns: The transfer function.
    Description: Used to provide the parallelT function with the logic of the transfer function.
'''
    
def parallelizeT():
    return lambda x: 1/(1+math.exp(-x))

'''
    parallelS
    Parameters:
    FCMs: A dictionary containing the FCMs to be parallelized along with the stabilizers to run simulation.
    Returns: Statistics of the execution of the jobs.
    Description: Takes multiple FCMs and parallelizes its simulation on a server. Module used for Parallel Python (pp): https://pypi.python.org/pypi/ppft
'''

def parallelS(FCMs):
    counter = 0
    print "Number of FCMs to parallelize: ", len(FCMs)
    ppservers = ()
    
    job_server = pp.Server(ppservers=ppservers) # creates the job server
    
    print "Starting pp with", job_server.get_ncpus(), "workers" # number of local processors
    
    start_time = time.time() # begin time
    
    # jobs - the tasks passed to the parallelize function
    jobs = [(fcm, job_server.submit(parallelizeS, (fcm, FCMs[fcm],),(simulation.stabilize, simulation.steps,simulation.changeTransferFunction,simulation.run,), ("simulation",))) for fcm in FCMs]    
    for fcm, job in jobs:
        counter += 1
        print "Simulation on FCM #",counter, "is"
        job() # the output of simulation
    
    print "\nTime elapsed: ", time.time() - start_time, "s\n\n" # end time
    return job_server.print_stats()

'''
    parallelT
    Parameters:
    job_count: An integer representing the number of times to parallilize the transfer function.
    Returns: Statistics of the execution of the jobs.
    Description: Parallelizes the transfer function by pushing it on a server. Module used for Parallel Python (pp): https://pypi.python.org/pypi/ppft
'''

def parallelT(job_count):
    ppservers = ()
    
    job_server = pp.Server(ppservers=ppservers) # creates the job server

    print "Starting pp with", job_server.get_ncpus(), "workers" # number of local processors
    
    start_time = time.time() # begin time
    
    # jobs - the tasks passed to the parallelize function
    jobs = [(i, job_server.submit(parallelizeT)) for i in range(job_count)]
    for i, job in jobs:
        print "Transfer function #", i, "is", job() # the lambda transfer function

    print "\nTime elapsed: ", time.time() - start_time, "s\n\n"
    job_server.print_stats()