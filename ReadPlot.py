import matplotlib.pyplot as plt
import numpy as np
import easygui, time
from mpl_toolkits.mplot3d import Axes3D
from threading import Thread
from collections import deque

REALTIMING = 1
rawdata = deque()
rw = deque()

def get_data():
    filename = "C:\Users\Arjuna Scagnetto\Documents\GitHub\Atti-Respiratori\estrazione2.txt"
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        if REALTIMING:
            time.sleep(.001)
        temp = line.replace('\n','').split('\t')
        rawdata.append(temp)
        rw.append(temp)
    return rawdata, rw

# Plot dinamico dei parametri flusso pressione
def animate_timeseries():
    plt.ion()
    #fig = plt.figure()
    fig, ax = plt.subplots(3)
    #ax = plt.axes()
    #ax = fig.add_subplot(111)
    ax[0].set_autoscale_on(True)
    ax[0].autoscale_view(True,True,True)
    ax[1].set_autoscale_on(True)
    ax[1].autoscale_view(True,True,True)
    ax[2].set_autoscale_on(True)
    ax[2].autoscale_view(True,True,True)
    #pressure_line, = ax.plot(pressure,'r')
    #flow_line, = ax.plot(flow,'b')
    #eadi_line, = ax.plot(eadi)
    pressure_line, = ax[0].plot(pressure,'r')
    flow_line, = ax[1].plot(flow,'b')
    eadi_line, = ax[2].plot(eadi,'g')
    
    t = np.linspace(0,100,1)
    for i in range(2000):    
        values = rawdata.popleft()[1:4]
        pressure.append(values[0])
        pressure.pop(0)
        flow.append(values[1])
        flow.pop(0)
        eadi.append(values[2])
        eadi.pop(0)
        #ax.set_xdata(range(i,i+100))
	pressure_line.set_ydata(pressure)
	flow_line.set_ydata(flow)
        eadi_line.set_ydata(eadi)
        ax[0].relim()
        ax[0].autoscale_view(True,True,True)
        ax[1].relim()
        ax[1].autoscale_view(True,True,True)
        ax[2].relim()
        ax[2].autoscale_view(True,True,True)
        #plt.xlim([i,i+1])
        #plt.ylim([0,100])
        #plt.autoscale_view(True,True,True)
        plt.draw()

def animate_cycles():
    plt.ion()
    fig = plt.figure()
    #fig, ax = plt.plot()
    ax = plt.axes()
    #ax = fig.add_subplot(111)
    #ax.set_autoscale_on(True)
    #ax.autoscale_view(True,True,True)
    cycle_line, = ax.plot(pressure,flow)
    for i in range(2000):    
        values = rw.popleft()[1:3]
        pressure.append(values[0])
        pressure.pop(0)
        flow.append(values[1])
        flow.pop(0)
	cycle_line.set_data(pressure,flow)
        #ax.relim()
        #ax.autoscale_view(True,True,True)
        plt.xlim([0,2000])
        plt.ylim([-10000,10000])
        #plt.autoscale_view(True,True,True)
        plt.draw()



t = Thread(target=get_data)
t.daemon = True
t.start()
time.sleep(1)
pressure = [0]*100
flow = [0]*100
eadi = [0]*100

#ts = Thread(target=animate_timeseries)
#ts.start()

animate_timeseries()
animate_cyles()
#tc = Thread(target=animate_cycles)
#tc.start()