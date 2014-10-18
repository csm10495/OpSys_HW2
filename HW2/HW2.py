#Operating Systems HW 2
#Charles Machalow...and theoretically others

import random
import sys

#Process Class
#Burst time: burst
#Process ID: pid
#Priority: priority

time = 0
class Process:
    
    #Constructor, makes a Process Object
    def __init__(self, burst, pid, priority, cpu_bound, io_time, b=None):
        self.burst = burst
        self.pid = pid
        self.priority = priority
        self.wait_time = 0         #time waiting in queue
        self.turnaround_time = 0   #total turnaround time
        self.run_time = 0          #time process has run so far (should == burst at end)
        self.running_cpu = -1      #if this is negative, the process isn't running
        self.cpu_bound = cpu_bound #this is True if this process is CPU bound, False if interactive
        
        #CPU Bound
        if self.cpu_bound and not b:
            self.b = 8
        elif not self.cpu_bound and not b:
            self.b = 0
        else:
            #b is set in constructor
            self.b = b

        self.io_time = io_time     #the amount of time the process is blocked on IO

    #gets cpu_bound
    def isCPUBound(self):
        return cpu_bound

    #gets b
    def getB(self):
        return self.b

    #returns IO blocking time (time not on the queue after burst)
    def getIOTime(self):
        return self.io_time

    #returns True if the process is IO bound (interactive)
    def isInteractive(self):
        return (not self.cpu_bound)

    #returns True if the process is CPU bound
    def isCPUBound(self):
        return self.cpu_bound

    #returns if the process is running on a CPU
    def isRunning(self):
        return self.running_cpu >= 0

    #if the process is not running, start it on cpu_num
    def startRunning(self, cpu_num):
        if self.isRunning():
            print "ERROR, process", self.pid, "already running on CPU (this shouldn't happen)", str(self.running_cpu)
        else:
            self.running_cpu = cpu_num

    #returns wait_time
    def getWaitTime(self):
        return self.wait_time

    #returns turnaround_time
    def getTurnaroundTime(self):
        return self.turnaround_time

    #returns priority
    def getPriority(self):
        return self.priority

    #returns PID
    def getPID(self):
        return self.pid

    #returns run_time
    def getRunTime(self):
        return self.run_time

    #returns burst
    def getBurst(self):
        return self.burst

    #increment priority by 1
    def incPriority(self):
        if self.priority > 0:
            self.priority=-1
            if(self.cpu_bound):
                print "Increased the priority of CPU - bound process ID", self.pid, "to", self.priority," due to aging"
            else:
                print "Increased the priority of Interactive - bound process ID", self.pid, "to", self.priority," due to aging"

    #increments wait_time by 1
    def incrementWaitTime(self):
        self.wait_time = self.wait_time + 1

    #increments turnaround_time by 1
    def incrementTurnaroundTime(self):
        self.turnaround_time = self.turnaround_time + 1

    #increments run_time by 1
    def incrementRunTime(self):
        self.run_time = self.run_time + 1

    #returns True if the process has finished its needed burst time
    #if run_time == burst
    def isDone(self):
        global time
        if self.burst <= self.run_time:
            if self.cpu_bound:
                print "[time",time,"ms] CPU bound process ID ", self.pid," terminated (avg turnaround time ", self.turnaround_time,"Total wait time",self.wait_time,"ms)"
            else:
                print "[time",time,"ms] Interactive process ID ", self.pid," terminated (avg turnaround time ", self.turnaround_time,"Total wait time",self.wait_time,"ms)"
        return self.burst <= self.run_time

#Priority Queue class based on a certain key
class cPQueue:
    
    #Constructor, initializes empty quque
    def __init__(self, sortNum):
        self._LQ = []
        self._WP = {}
        self.sortNum = sortNum

    #adds an item to _LQ, sorts as it goes
    def addItem(self, item):
        #go through each item in _List_Queue and add it

        #Special case for previously empty _LQ
        if len(self._LQ) == 0:
            self._LQ.append(item)
            return True

        for i in range(len(self._LQ)):
            #FCFS
            if self.sortNum == 0:
                #Compare Pids
                if self._LQ[i].getPID() > item.getPID():
                    self._LQ.insert(i, item)
                    return True
            #SJF
            if self.sortNum == 1:
                #Compare burst time
                p = self._LQ[i]
                if item.getBurst() < p.getBurst():
                    self._LQ.insert(i, item)
                    return True
            #P_SJF
            if self.sortNum == 2:
                p = self._LQ[i]
                if item.getBurst() < p.getBurst() - p.getRunTime():
                    self._LQ.insert(i, item)
                    return True        
            #P_RR
            if self.sortNum == 3:
                #allow the process to be added to the end of the queue
                pass       
            
            #Preemptive Priority
            if self.sortNum == 4:
                p = self._LQ[i]
                #lower number means higher priority
                if item.getPriority() < p.getPriority():
                    self._LQ.insert(i, item)
                    return True
                #else, the item should get added to the end of the list (FCFS)
            
                

        #If all else fails, add to end of List
        self._LQ.append(item)
        return True
            
    #Peeks the 0th value of _LQ
    #returns None on failure
    def peekTop(self):
        if not len(self._LQ) == 0:
            return self._LQ[0]
        else:
            return None

    #Peeks item [val] in _LQ
    #Will be useful for multiple CPUs
    def peekValue(self, val):
        if len(self._LQ) > val:
            return self._LQ[val]
        else:
            print "Index out of bound exception on peekValue(", val, ") _LQ has a len of", len(self._LQ)
            return None

    #Pops the 0th value of _LQ
    #returns None on failure
    def popTop(self):
        if not len(self._LQ) == 0:
            return self._LQ.pop(0)
        else:
            return None

    #Returns if the _LQ
    def isEmpty(self):
        return len(self._LQ) == 0

    #increments all Turnaround times in Queue
    def incTurnAroundTimes(self):
        for i in self._LQ:
            i.incrementTurnaroundTime()

    #increments all waittimes in Queue
    #(for ALL processes)
    def incWaitTimes(self):
        for i in self._LQ:
            i.incrementWaitTime()

    #returns elements in cPQ
    def getLength(self):
        return len(self._LQ)

    #returns last element in cPQ
    def getLastElement(self):
        return self._LQ[-1]

    #[this should be called by the current running algorithm, when process burst time reached]
    #add a user simulated process that re enters the queue after a set time
    def addWaitingProcess(process):
        self._WP[process] = waitTime
        
    #[this should be called after EVERY time interval]
    #update the waiting user simulated processes
    def updateWaitingProcesses():
        for key, value in self._WP:
            #decrease the remaining wait time
            value -= 1
            
            #if the remaining wait time is less than 0, re-introduce to pq
            if(value < 0):
                self.addItem(p)
                del self._WP[key]
            #otherwise update the wait time
            else:
                self._WP[key] = value
       
    #If wait time mod 1200 == 0 increase priority
    def incPriorities(self):
        for i in self._LQ:
            if i.getWaitTime() % 1200 == 0:
                i.incPriority()
        t_cPQ = cPQueue(4)
        for i in self._LQ:
            t_cPQ.addItem(i)
        
        self._LQ = t_cPQ._LQ  #ugly code...


#A CPU class
class CPU:

    #Constructor that does set a running process (p)
    def __init__(self, p=None):
        self.runningprocess = p

    #Attempts to make a context switch
    #Returns True and changes the running process if a switch occurs
    #Returns False if a context switch is not necessary and a switch doesn't
    #occur
    def contextSwitch(self, new_p):
        if not new_p:
            self.runningprocess = None
        if not self.runningprocess:
            self.runningprocess = new_p
            return True
        if self.runningprocess.getPID() == new_p.getPID():
            return False
        else:
            self.runningprocess = new_p
            return True

    #Returns True if this CPU is in use
    def isInUse(self):
        if self.runningprocess == None:
            return False
        else:
            return True

    #increments necessary times of process in CPU
    def incrementTimes(self):
        self.runningprocess.incrementRunTime()
        self.runningprocess.incrementTurnaroundTime()

    #returns the currently running process
    def getRunningProcess(self):
        return self.runningprocess


#gets a list of processes of size n
#~80% of them are interactive (20 - 200ms burst)
#blocking time of 1000-4500ms
#other 20% is CPU bound (200 - 3000ms)
#blocking ime of 1200-3200ms
def getProcessList(n):
    process_list = []
    for i in range(n):
        #interactive
        if i < n * .8:
            process_list.append(Process(random.randint(20, 200), i, random.randint(0, 4), False, random.randint(1000, 4500)))
        else:
            #CPU bound
            process_list.append(Process(random.randint(200, 3000), i, random.randint(0, 4), True, random.randint(1200, 3200)))

    random.shuffle(process_list)
    return process_list

def getProcess(b):
    return Process(random.randint(200, 3000), i, random.randint(0, 4), True, random.randint(1200, 3200), b) 

#returns a list of n [CPUs, 0]
def getCPUList(n):
    lst = []
    for i in range(n):
        lst.append([CPU(), 0])
    return lst

#returns True if a CPU is busy
def aCPUIsBusy(CPUs):
    for i in CPUs:
        if i[0].isInUse():
            return True
    return False

#cPQ is a cPriorityQueue
#n_CPU is the number of CPUs
#Non Preemptive SJF
def nonPreemptive(cPQ, n_CPU):  
    global time
    CPUs = getCPUList(n_CPU)

    #initial adding
    for i in CPUs:
        if cPQ.isEmpty():
            break
        i[0].contextSwitch(cPQ.popTop())
        time += 1
        i[0].incrementTimes()

    cPQ.incWaitTimes()
    cPQ.incTurnAroundTimes()

    while not cPQ.isEmpty():
        count = 1
        for i in CPUs:
            #the process on this CPU is done and we have another to give it
            if i[0].getRunningProcess().isDone() and not cPQ.isEmpty():
                p = i[0].getRunningProcess()
                time += 1
                i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH
                time += 1
                print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"
            if not i[0].getRunningProcess().isDone():
                i[0].incrementTimes()
            count += 1
            time+=1
        
        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()

    #gets number of currently alive CPUs
    num_alive_CPUs = 0
    for i in CPUs:
        if i[0].isInUse():
            num_alive_CPUs += 1


    #Clear out processes already in CPUs
    while True:
        inuse = False
        count = 1
        for i in CPUs:
            if i[0].isInUse():
                inuse = True
                i[0].incrementTimes()

                if i[0].getRunningProcess().isDone():
                    p = i[0].getRunningProcess()
                    time += 1
                    i[0].contextSwitch(cPQ.popTop())  #switches to None
                    if p.cpu_bound:
                        print "[time",time,"ms] CPU bound process ID ", p.getPID()," CPU burst done (turnaround time ", p.getTurnaroundTime(),"Total wait time",p.getWaitTime(),"ms)"
                    else:
                        print "[time",time,"ms] Interactive bound process ID ", p.getPID()," CPU burst done (turnaround time ", p.getTurnaroundTime(),"Total wait time",p.getWaitTime(),"ms)"
                    num_alive_CPUs -= 1
                    #print "PID:", p.getPID(), "Completed on CPU", count, " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()
            count += 1
        if not inuse or inuse is False or num_alive_CPUs == 0:
            break
        time+=1


#[this should be called whenever a process ends]
#checks if the process should be addded to the waitingProcessDict
def simulateUser(cPQ, process):
    
    #add the process SECOND, other wise the wait time will be updated prematurely
    if process.isCPUBound() and process.getB() > 0:
        p = getProcess( process.getB() - 1 )
        cPQ.addWaitingProcess(p)
    

#cPQ is a cPriorityQueue
#n_CPU is the number of CPUs
#SJF Preemptive
def Preemptive(cPQ, n_CPU):  
    global time
    CPUs = getCPUList(n_CPU)

    #initial adding
    for i in CPUs:
        if cPQ.isEmpty():
            break
        i[0].contextSwitch(cPQ.popTop())
        time += 1
        i[0].incrementTimes()

    cPQ.incWaitTimes()
    cPQ.incTurnAroundTimes()

    while not cPQ.isEmpty():
        count = 1
        for i in CPUs:
            if not cPQ.isEmpty():
                cPQ.addItem(i[0].getRunningProcess())  #add current CPU process back to cPQ to see if it should be preempted
                if (cPQ.peekTop().getPID() != i[0].getRunningProcess().getPID()):
                    #PREEMPTION
                    p = i[0].getRunningProcess()
                    time += 1
                    i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH BECAUSE OF PREEMPTION
                    time += 1
                    print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"
                else:
                    cPQ.popTop()

            if i[0].getRunningProcess().isDone() and not cPQ.isEmpty():
                p = i[0].getRunningProcess()
                time+=1
                i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH BECAUSE OF BURST COMPLETION
                time+=1
                print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"

            if not i[0].getRunningProcess().isDone():  #if the current process on CPU i[0] is not done
                i[0].incrementTimes()

            count += 1
            time+=1

        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()

    #gets number of currently alive CPUs
    num_alive_CPUs = 0
    for i in CPUs:
        if i[0].isInUse():
            num_alive_CPUs += 1

    #Clear out processes already in CPUs
    while True:
        inuse = False
        count = 1
        for i in CPUs:
            if i[0].isInUse():
                inuse = True
                i[0].incrementTimes()

                if i[0].getRunningProcess().isDone():
                    p = i[0].getRunningProcess()
                    time += 1
                    i[0].contextSwitch(cPQ.popTop())  #switches to None
                    if p.cpu_bound:
                        print "[time",time,"ms] CPU bound process ID ", p.getPID()," CPU burst done (turnaround time ", p.getTurnaroundTime(),"Total wait time",p.getWaitTime(),"ms)"
                    else:
                        print "[time",time,"ms] Interactive bound process ID ", p.getPID()," CPU burst done (turnaround time ", p.getTurnaroundTime(),"Total wait time",p.getWaitTime(),"ms)"
                        #print "PID:", p.getPID(), "Completed on CPU", count, " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()
                    num_alive_CPUs -= 1
            count += 1
        if not inuse or num_alive_CPUs == 0:
            break
        time+=1

def PreemptivePriority(cPQ, n_CPU):
    
    global time
    dt = 0 #needed to update priority
    CPUs = getCPUList(n_CPU)

    #initial adding
    for i in CPUs:
        if cPQ.isEmpty():
            break
        i[0].contextSwitch(cPQ.popTop())
        time += 1
        i[0].incrementTimes()

    cPQ.incWaitTimes()
    cPQ.incTurnAroundTimes()


    while not cPQ.isEmpty():
        count = 1
        for i in CPUs:
            if not cPQ.isEmpty():
                cPQ.addItem(i[0].getRunningProcess())  #add current CPU process back to cPQ to see if it should be preempted
                if (cPQ.peekTop().getPID() != i[0].getRunningProcess().getPID()):
                    #PREEMPTION
                    p = i[0].getRunningProcess()
                    time += 1
                    dt+=1
                    i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH BECAUSE OF PREEMPTION
                    time += 1
                    dt+=1
                    print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"
                else:
                    cPQ.popTop()

            if i[0].getRunningProcess().isDone() and not cPQ.isEmpty():
                p = i[0].getRunningProcess()
                time+=1
                dt+=1
                i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH BECAUSE OF BURST COMPLETION
                time+=1
                dt+=1
                print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"

            if not i[0].getRunningProcess().isDone():  #if the current process on CPU i[0] is not done
                i[0].incrementTimes()

            count += 1
            time+=1
            dt+=1
        if(dt-1200)>=0:#check to see if time to increase priority
            for p in cPQ:
                p.incPriority()
            dt = 0
        
        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()

    #gets number of currently alive CPUs
    num_alive_CPUs = 0
    for i in CPUs:
        if i[0].isInUse():
            num_alive_CPUs += 1

    #Clear out processes already in CPUs
    while True:
        inuse = False
        count = 1
        for i in CPUs:
            if i[0].isInUse():
                inuse = True
                i[0].incrementTimes()

                if i[0].getRunningProcess().isDone():
                    p = i[0].getRunningProcess()
                    time += 1
                    i[0].contextSwitch(cPQ.popTop())  #switches to None
                    if p.cpu_bound:
                        print "[time",time,"ms] CPU bound process ID ", p.getPID()," CPU burst done (turnaround time ", p.getTurnaroundTime(),"Total wait time",p.getWaitTime(),"ms)"
                    else:
                        print "[time",time,"ms] Interactive bound process ID ", p.getPID()," CPU burst done (turnaround time ", p.getTurnaroundTime(),"Total wait time",p.getWaitTime(),"ms)"
                        #print "PID:", p.getPID(), "Completed on CPU", count, " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()
                    num_alive_CPUs -= 1
            count += 1
            time+=1
            dt+=1
            
        if not inuse or num_alive_CPUs == 0:
            break
        time+=1
        dt+=1
    if(dt-1200)>=0:#check to see if time to increase priority
        for p in cPQ:
            p.incPriority()
        dt = 0


def RoundRobin(cPQ, n_CPU, timeslice=100):
    CPUs = getCPUList(n_CPU)

    #initial adding
    for i in CPUs:
        if cPQ.isEmpty():
            break
        i[0].contextSwitch(cPQ.popTop())
        i[0].incrementTimes()

    cPQ.incWaitTimes()
    cPQ.incTurnAroundTimes()

    dt = [0 for i in range(n_CPU)]
    while not cPQ.isEmpty():
        index = 0        # Keep track of the current deltaTime index
        count = 1        # Keep track of the current CPU number

        for i in CPUs:            
            resetDelta = False         
            dt[index] += 1 # Update delta time
            
            # BURST CHECK
            if i[0].getRunningProcess().isDone() and not cPQ.isEmpty():                
                resetDelta = True                     # SINCE THE PROCESS HAS FINISHED, RESET DT FOR THE NEXT PROCESS
                p = i[0].getRunningProcess() 
                i[0].contextSwitch(cPQ.popTop())      # CONTEXT SWITCH BECAUSE OF BURST COMPLETION
            
                print "[burst][time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"
                print "PID:", p.getPID(), "Completed on CPU", count, " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()
                
            # TIMESLICE CHECK
            if not cPQ.isEmpty():                     # if other processes still exist
                if(dt[index] >= timeslice):
                                                      # ROUND ROBIN PREEMPTION OCCURS
                    resetDelta = True                 # need to reset deltaTime[i]
                    p = i[0].getRunningProcess()      # STORE THE OLD PROCESS (ALREADY BACK IN cPQ)
                    cPQ.addItem(p)                    # Add this to the end of the cPQ
                    i[0].contextSwitch(cPQ.popTop())  # CONTEXT SWITCH BECAUSE OF PREEMPTION
                    print "[slice][time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"

            if not i[0].getRunningProcess().isDone():  #if the current process on CPU i[0] is not done
                i[0].incrementTimes()
            
            if resetDelta:      # if the time needs to be reset due to preemption,                
                dt[index] = 0   # Increment the deltaTime for the process on the current cpu                

            count += 1 
            index += 1          # increment current dt index

        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()

    #Clear out processes already in CPUs
    while True:
        inuse = False
        count = 1
        for i in CPUs:
            if i[0].isInUse():
                inuse = True
                i[0].incrementTimes()
                if i[0].getRunningProcess().isDone():
                    p = i[0].getRunningProcess()
                    i[0].contextSwitch(cPQ.popTop())  #switches to None
                    print "PID:", p.getPID(), "Completed on CPU", count, " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()
            count += 1
        if not inuse:
            break

#prints help, usage
def printHelp():
    print "Usage:"
    print "HW2.py <(int) Algorithm type> <(int) Number of processess> <(int) Number of processors> <(int)timeslice>"
    print "Algorithm Types:"
    print "     1: SJF No Preemption"
    print "     2: SJF With Preemption"
    print "     3: Round Robin"
    print "     4: Preemptive Priority"
    print "Number of Processes: 1...n"
    print "Number of Processors: 1...n"
    print "Timeslice: timeslice for Round Robin, ignored otherwise"
    print "If No arguments provided: Autoruns 'HW2.py 1 14 4'"
    print "SJF No Preemption with 14 processes and 4 processors"

#runs according to command-line arguments
def run(algorithm, num_processes, n_CPU, timeslice=100):
    if algorithm > 0 and algorithm <=4 and num_processes > 0 and n_CPU > 0:
        cPQ = cPQueue(algorithm)
        a = getProcessList(num_processes)
        for i in a:
            if(i.isCPUBound()):#print that an item has been added
                print "CPU-bound process ",i.getPID()," entered the ready queue (requires ",i.getBurst(),"ms CPU time; priority", i.getPriority(),")"
            else:
                print "Interactive process ",i.getPID()," entered the ready queue (requires ",i.getBurst(),"ms CPU time; priority", i.getPriority(),")"
            cPQ.addItem(i)
        if algorithm == 1:
            print "Non Preemptive SJF with", num_processes, "Processes,", n_CPU, "Processors"
            nonPreemptive(cPQ, n_CPU)
        elif algorithm == 2:
            print "Preemptive SFJ with", num_processes, "Processes,", n_CPU, "Processors"
            Preemptive(cPQ, n_CPU)
        elif algorithm == 3:
            print "Round Robin with ", num_processes, "Processes,", n_CPU, "Processors,", timeslice, "ms timeslice"
            RoundRobin(cPQ, n_CPU)
        elif algorithm == 4:
            print "Preemptive Priority with", num_processes, "Processes,", n_CPU, "Processors"
            PreemptivePriority(cPQ, n_CPU)
    else:
        print "Bad input parameters"
        print "(1-4) (1-n) (1-n) <1-n>"

done = False

if len(sys.argv) == 2 and (sys.argv[1] == "?" or sys.argv[1] == "/?" or sys.argv[1] == "help"):
    printHelp()
    done = True

algorithm = -1
num_processes = -1
n_CPU = -1
timeslice = 100

if len(sys.argv) == 1:
    print "Going with defaults: SJF No Preemption with 14 processes and 4 processors"
    algorithm = 1
    num_processes = 14
    n_CPU = 4

if len(sys.argv) >= 4:
    algorithm = int(sys.argv[1])
    num_processes = int(sys.argv[2])
    n_CPU = int(sys.argv[3])
    if algorithm == 4 and len(sys.argv) == 4:
        print "Assuming RR timeslice = 100"

if len(sys.argv) == 5:
    timeslice = int(sys.argv[4])

if not done:
    run(algorithm, num_processes, n_CPU, timeslice)
print "Done!"
