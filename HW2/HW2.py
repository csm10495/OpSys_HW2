#Operating Systems HW 2
#Charles Machalow...and theoretically others

import random

#Process Class
#Burst time: burst
#Process ID: pid
#Priority: priority
class Process:
    
    #Constructor, makes a Process Object
    def __init__(self, burst, pid, priority, cpu_bound, io_time):
        self.burst = burst
        self.pid = pid
        self.priority = priority
        self.wait_time = 0         #time waiting in queue
        self.turnaround_time = 0   #total turnaround time
        self.run_time = 0          #time process has run so far (should == burst at end)
        self.running_cpu = -1      #if this is negative, the process isn't running
        self.cpu_bound = cpu_bound #this is True if this process is CPU bound, False if interactive
        self.io_time = io_time     #the amount of time the process is blocked on IO

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
        self.priority+=1
        if(self.cpu_bound):
            print "Increased the priority of CPU - bound process ID", self.pid, "to", self.priority," due to aging"
        else:
            print "Increased the priority of CPU - bound process ID", self.pid, "to", self.priority," due to aging"

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
        return self.burst == self.run_time

#Priority Queue class based on a certain key
class cPQueue:
    
    #Constructor, initializes empty quque
    def __init__(self, sortNum):
        self._LQ = []
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
    CPUs = getCPUList(n_CPU)

    #initial adding
    for i in CPUs:
        if cPQ.isEmpty():
            break
        i[0].contextSwitch(cPQ.popTop())
        i[0].incrementTimes()

    cPQ.incWaitTimes()
    cPQ.incTurnAroundTimes()

    while not cPQ.isEmpty():
        count = 1
        for i in CPUs:
            #the process on this CPU is done and we have another to give it
            if i[0].getRunningProcess().isDone() and not cPQ.isEmpty():
                p = i[0].getRunningProcess()
                i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH
                print "PID:", p.getPID(), "Completed on CPU", count, " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()
            if not i[0].getRunningProcess().isDone():
                i[0].incrementTimes()
            count += 1
        
        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()

#cPQ is a cPriorityQueue
#n_CPU is the number of CPUs
#SJF Preemptive
def Preemptive(cPQ, n_CPU):  
    CPUs = getCPUList(n_CPU)

    #initial adding
    for i in CPUs:
        if cPQ.isEmpty():
            break
        i[0].contextSwitch(cPQ.popTop())
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
                    i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH BECAUSE OF PREEMPTION
                    print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"
                else:
                    cPQ.popTop()

            if i[0].getRunningProcess().isDone() and not cPQ.isEmpty():
                p = i[0].getRunningProcess()
                i[0].contextSwitch(cPQ.popTop())  #CONTEXT SWITCH BECAUSE OF BURST COMPLETION
                print "[time",time,"ms] context switch(swapping out process ID ", p.getPID()," for process ID", i[0].getRunningProcess().getPID(),")"

            if not i[0].getRunningProcess().isDone():  #if the current process on CPU i[0] is not done
                i[0].incrementTimes()

            count += 1

        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()





def RoundRobin(timeslice):

    while not cPQ.isEmpty():
        tDelta = 0
        p = cPQ.popTop() #current process in the queue
        while tDelta < timeslice:
            tDelta += 1
        
            #check if the process is still running
            if(not p.isDone()):
                p.incrementRunTime()
                p.incrementTurnaroundTime() #need to do this because it has been popped from cPQ
                cPQ.incWaitTimes()
                cPQ.incTurnAroundTimes()
            else:
                break
        
        #if the process has not finished, re add it to the queue
        if(not p.isDone()):
            cPQ.addItem(p)
            if (p.getPID() != cPQ.peekTop().getPID()):
                print "This Process has been Preempted: PID:", p.getPID(), " Burst:", p.getBurst(), " RunTime:", p.getRunTime()
            else:
                print "Process", p.getPID(), "will continue running because it is still first in queue"     #can't preempt yourself
            print "Finished: PID:", p.getPID(), " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()





a = getProcessList(14)

cPQ = cPQueue(2)

time = 0
for i in a:
    if(i.isCPUBound()):#print that an item has been added
        print "CPU-bound process ",i.getPID()," entered the ready queue (requires ",i.getBurst(),"ms CPU time; priority", i.getPriority(),")"
    else:
        print "Interactive process ",i.getPID()," entered the ready queue (requires ",i.getBurst(),"ms CPU time; priority", i.getPriority(),")"
    cPQ.addItem(i)


Preemptive(cPQ, 4)
