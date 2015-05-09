import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
import os,sys
from collections import deque

nsPlot = 20 # number of SubPlot

def gen_subplot(start,finish,data,nsPlot,nCicli):
    for i in range(start,finish+1):
        fig = plt.figure()
        for j in range(nCicli):
            cycle = np.asarray(data.pop())
            plt.subplot(nsPlot/2,2,j)
            plt.plot(cycle[:,1],cycle[:,2],'r')
            plt.xlabel('Pressione')
            plt.ylabel('Flusso')
        dir = os.path.dirname('images/')
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = "".join(('images/image-',str(nsPlot),'-',str(i)))
        print "Saving",filename 
        plt.savefig(filename)
        plt.close()

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

for i in range(length):
    if st[i] == 1:
            if c == 0:
                    d.append(l)
                    l = []
                    c = 1
            l.append(['r',pr[i],fl[i]])
    else:
            if c == 1:
                    c = 0
            l.append(['g',pr[i],fl[i]])

# append dell'ultimo ciclo
d.append(l)

nIm = len(d) # Numero di Immagini

print '\n',nIm,'cicli a blocchi di ',nsPlot
print 'sono',nIm//nsPlot, " immagini da ", nsPlot
print "e 1 immagine da", nIm%nsPlot,'\n'

#gen_subplot(1,nIm//nsPlot,d,nsPlot,nsPlot)

if nIm%nsPlot != 0:
    gen_subplot(nIm//nsPlot+1,nIm//nsPlot+1,d,nsPlot,nIm%nsPlot)

