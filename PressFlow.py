import matplotlib.pyplot as plt
import numpy as np
import os
from collections import deque

from mpl_toolkits.axes_grid1.anchored_artists import AnchoredText

# !!!! EVEN NUMBER ONLY !!!
nsPlot = 6 # number of SubPlot 
plotVar = 1

def gen_subplot(start,finish,data,nsPlot,nCicli):
    font = {'family':'serif','color':'darkred','weight':'normal','size':16,}
    for i in range(start,finish+1):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('Pressione')
        ax.set_ylabel('Flusso')
        at = AnchoredText("Figure 1a",loc=2, prop=dict(size=16), frameon=True)
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        ax.add_artist(at)
        for j in range(nCicli):
            cycle = np.asarray(data.pop())
            fig.add_subplot(nsPlot/2,2,j)
            plt.plot(cycle[:,1],cycle[:,2],'r')
            #plt.text(2, 0.65, 'prova', fontdict=font)
        dir = os.path.dirname('images/')
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = "".join(('images/image-',str(nsPlot),'-',str(i)))
        print "Saving",filename 
        #plt.savefig(filename,dpi=300)
        plt.savefig(filename)
        plt.close()

def build_data():
    filename = "estrazione.txt"
    f = open(filename,"r")
    rows = f.readlines()
    length = len(rows)
    v = np.ndarray(shape=(length,3),dtype=float)
    for i in range(length):
        v[i,:]=rows[i].replace('\n','').split('\t',2)
    st = v[:,0] # States 0 inspirio 1 espirio
    pr = v[:,1] # Pressure
    fl = v[:,2] # Flow
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
            l.append(['r',pr[i],fl[i],i+1])
        else:
            if c == 1:
                c = 0
            l.append(['g',pr[i],fl[i],i+1])
    # append of the last cycle
    d.append(l)
    return d


deque = build_data()
nIm = len(deque) # Number of Images
print '\n',nIm,'cicli a blocchi di ',nsPlot
print 'sono',nIm//nsPlot, " immagini da ", nsPlot
print "e 1 immagine da", nIm%nsPlot,'\n'

print deque[-1][-1]

if plotVar:
    gen_subplot(1,nIm//nsPlot,deque,nsPlot,nsPlot)
    if nIm%nsPlot != 0:
        gen_subplot(nIm//nsPlot+1,nIm//nsPlot+1,deque,nsPlot,nIm%nsPlot)

