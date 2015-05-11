import matplotlib.pyplot as plt
import numpy as np
import os
from collections import deque


# !!!! EVEN NUMBER ONLY !!!
nsPlot = 10 # number of SubPlot 
plotVar = 1

def gen_subplot(Num_of_images,data):
    for i in range(0,Num_of_images):
        f, ax = plt.subplots(2)
        ax[0].set_xlabel('Pressione')
        ax[0].set_ylabel('Flusso')
        cycle = np.asarray(data[i])
        time_len = len(cycle[:,0])
        t = np.linspace(0,1,time_len)
        print len(t),len(cycle[:,1])
        ax[0].plot(cycle[:,1],cycle[:,2],'r')
        ax[1].plot(t,cycle[:,1],t,cycle[:,2],t,cycle[:,3])
        dir = os.path.dirname('images/')
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = "".join(('images/image-','-',str(i)))
        print "Saving",filename 
        plt.savefig(filename)
        plt.close()

def build_data():
    filename = "estrazione2.txt"
    f = open(filename,"r")
    rows = f.readlines()
    length = len(rows)
    v = np.ndarray(shape=(length,4),dtype=float)
    for i in range(length):
        v[i,:]=rows[i].replace('\n','').split('\t',3)
    st = v[:,0] # States 0 inspirio 1 espirio
    pr = v[:,1] # Pressure
    fl = v[:,2] # Flow
    ed = v[:,3] # EDI
    c = 1
    d = deque()
    l = []
    #np.split(x, np.nonzero(np.diff(x) == 1)[0]+1)
    for i in range(length):
        if st[i] == 1:
            if c == 0:
                d.append(l)
                l = []
                c = 1
            l.append([i+1,pr[i],fl[i],ed[i]])
        else:
            if c == 1:
                c = 0
            l.append([i+1,pr[i],fl[i],ed[i]])
    # append of the last cycle
    d.append(l)
    return d


deque = build_data()
nIm = len(deque) # Number of Images
print '\n',nIm,'immagini'
print 'ULTIMO APPEND: ',deque[-1][-1]

if plotVar:
    gen_subplot(nIm,deque)
