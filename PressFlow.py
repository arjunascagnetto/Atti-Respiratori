import matplotlib.pyplot as plt
import numpy as np
import os
from collections import deque
from matplotlib.font_manager import FontProperties

# zero for testing only
plotVar = 1

def nta_file_cleaner():
    filename = '001_ServoCurveData_0000.nta'
    f = open(filename,'r')
    lines = f.readlines()
    dat = deque()
    for line in lines:
        if not line.startswith('%'):
            dat.append(line.replace('\n','').split('\t',8))
    v = np.ndarray(shape=(len(dat),8),dtype=float)
    for i in range(len(dat)):
        for j in range(3,7): # prende solo dalla colonna 4 alla 7
            v[i,j]=float(dat[i][j])
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
        print "Saving",filename 
        if plotVar:
            plt.savefig(filename)
        plt.close()

def build_data():
    filename = "estrazione2.txt"
    f = open(filename,"r")
    rows = f.readlines()
    length = len(rows)
    v = np.ndarray(shape=(length,4),dtype=float)
    for i in range(length):
        v[i,:] = rows[i].replace('\n','').split('\t',4)
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


#v = nta_file_cleaner()
deque = build_data()
nIm = len(deque) # Number of Images
gen_subplot(nIm,deque)
