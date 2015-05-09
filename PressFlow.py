import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
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

nIm = len(d) # Numero di Immagini

print nIm,type(d),np.shape(d),'\n'

for i in range(nIm):
    
    cycle1 = np.asarray(d.pop())
    cycle2 = np.asarray(d.pop())
    cycle3 = np.asarray(d.pop())
    cycle4 = np.asarray(d.pop())
    cycle5 = np.asarray(d.pop())
    cycle6 = np.asarray(d.pop())
    
    plt.subplot(321)
    plt.plot(cycle1[:,1],cycle1[:,2],'r')
    plt.subplot(322)
    plt.plot(cycle2[:,1],cycle2[:,2],'r')
    plt.subplot(323)
    plt.plot(cycle3[:,1],cycle3[:,2],'r')
    plt.subplot(324)
    plt.plot(cycle4[:,1],cycle4[:,2],'r')
    plt.subplot(325)
    plt.plot(cycle5[:,1],cycle5[:,2],'r')
    plt.subplot(326)
    plt.plot(cycle6[:,1],cycle6[:,2],'r')
    
    
    #plt.xlabel('Pressione')
    #plt.ylabel('Flusso')
    plt.show()
    raw_input("Press cuel to continue...")