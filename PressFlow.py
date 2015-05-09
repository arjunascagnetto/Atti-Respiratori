import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
import os
from collections import deque


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

inspirio = 0 # Inspirio

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

# Manca l'ultimo ciclo da aggiungere in append
d.append(l)

nIm = len(d) # Numero di Immagini
nsPlot = 6

print nIm,type(d),np.shape(d),'\n'

for i in range(1,nIm//nsPlot):
    fig = plt.figure()
    for j in range(nsPlot):
        cycle = np.asarray(d.pop())
        plt.subplot(3,2,j)
        plt.plot(cycle[:,1],cycle[:,2],'r')
        plt.xlabel('Pressione')
        plt.ylabel('Flusso')
    dir = os.path.dirname('images/')
    if not os.path.exists(dir):
        os.makedirs(dir)
    filename = "".join(('images/image',str(i)))
    print "Saving",filename 
    plt.savefig(filename)
    plt.close()    
        
        