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

        if(item.isCPUBound()):#print that an item has been added
            print "CPU-bound process ",item.getPID()," entered the ready queue (requires ",item.getBurst(),"ms CPU time; priority", item.getPriority(),")"
        else:
            print " Interactive process ",item.getPID()," entered the ready queue (requires ",item.getBurst(),"ms CPU time; priority", item.getPriority(),")"
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
    #(for processes past [0])
    def incWaitTimes(self):
        first = True
        for i in self._LQ:
            if first:
                first = False
                continue
            else:
                i.incrementWaitTime()

    #returns elements in cPQ
    def getLength(self):
        return len(self._LQ)

    #returns last element in cPQ
    def getLastElement(self):
        return self._LQ[-1]



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

a = getProcessList(14)

#Entry Point
cPQ = cPQueue(1)

print "This is a test of FCFS, Lower PID -> Earlier Process"

time = 0
for i in a:
    cPQ.addItem(i)

while not cPQ.isEmpty():

    #process is still running
    if (not cPQ.peekTop().isDone()):
        cPQ.peekTop().incrementRunTime()
        cPQ.incWaitTimes()
        cPQ.incTurnAroundTimes()
    else:
        p = cPQ.popTop()
        print "PID:", p.getPID(), " Burst:", p.getBurst(), " RunTime:", p.getRunTime(), " Only took:", p.getTurnaroundTime(), " WaitTime:", p.getWaitTime()



