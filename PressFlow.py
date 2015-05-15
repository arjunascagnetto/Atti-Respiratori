import matplotlib.pyplot as plt
import numpy as np
import os
from collections import deque
from matplotlib.font_manager import FontProperties
import easygui

# zero for testing only
plotVar = 1

def nta_file_parser():
    filename = easygui.fileopenbox()
    #filename = '001_ServoCurveData_0000.nta'
    f = open(filename,'r')
    lines = f.readlines()
    dat = deque()
    for line in lines:
        if not line.startswith('%'):
            dat.append(line.replace('\n','').split('\t',8))
    v = np.ndarray(shape=(len(dat),4),dtype=float)
    for i in range(len(dat)):
        for j in range(3,7): # prende solo le colonne 4 5 6 7 
            v[i-3,j-3]=float(dat[i][j])
    return v

def ndata(data2norm):
    data2norm = data2norm/np.max(np.abs(data2norm))
    return data2norm

def gen_subplot(Num_of_images,data):
    for i in range(0,Num_of_images):
        fontP = FontProperties()
        fontP.set_size('small')
        f, ax = plt.subplots(2)
        ax[0].set_xlabel('Pressione')
        ax[0].set_ylabel('Flusso')
        cycle = np.asarray(data[i])
        start = cycle[0,0]
        end = cycle[-1,0]
        t = np.arange(start,end+1,1)
        ax[0].plot(cycle[:,1],cycle[:,2],'k')
        ax[1].plot(t,ndata(cycle[:,1]),'b',label='Pressione')
        ax[1].plot(t,ndata(cycle[:,2]),'r',label='Flusso')
        ax[1].plot(t,ndata(cycle[:,3]),'g',label='Edi')
        ax[1].legend(loc='lower right',prop = fontP)
        ax[0].set_title(('from',str(start),'to',str(end)))
        ax[1].set_xlabel('Tempo')
        ax[1].set_ylim(-1.2,1.2)
        ax[1].set_xlim(start,end)
        dir = os.path.dirname('images/')
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = "".join(('images/image','-',str(i+1)))
        if plotVar:
            print "Saving",filename
            plt.savefig(filename)
        plt.close()

def build_data(v):
    length = len(v)
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



vector = nta_file_parser()
print len(vector),vector.shape,type(vector)
deque = build_data(vector)
print len(deque),type(deque)
nIm = len(deque) # Number of Images
gen_subplot(nIm,deque)
