# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:37:31 2016

Using PYPOWER to estimate the impact of small variations in the 
obtained angles and voltages.
"""

import os
import pypower.api as pypo # to install, just pip install PYPOWER
import case14_mod
from numpy import zeros, hstack, transpose
import matplotlib.pyplot as plt

#import matplotlib as matplot

dlt_vec   = [0.05, -0.05, 0.10, -0.10, 0.50, -0.50]
ppc0      = case14_mod.case14_mod(busN = 1,dlt = 0, op_change=1) # trivial case: original solutin
#ppopt0    = pypo.ppoption(PF_ALG=2, VERBOSE=0,
#                          OUT_ALL      = False,
#                          OUT_ALL_LIM  = False,
#                          OUT_AREA_SUM = False,
#                          OUT_BRANCH   = False,
#                          OUT_BUS      = False,
#                          OUT_GEN      = False,
#                          OUT_LINE_LIM = False,
#                          OUT_PG_LIM   = False,
#                          OUT_QG_LIM   = False,
#                          OUT_SYS_SUM  = False,
#                          OUT_V_LIM    = False) # Careful: have to use Newton Method!!!
ppopt0    = pypo.ppoption(PF_ALG=2, VERBOSE=0, OUT_ALL=0) # Careful: have to use Newton Method!!!
r0        = pypo.runpf(ppc0, ppopt0)       
m1        = r0[0]['gen'][:,2][1:]
p0        = [m1 for i in range(0,8)] 
mtr       = zeros([8,4,len(dlt_vec)]) 

j = 1
for j in range(0,len(dlt_vec)):
    tmp = 0
    for i in range(0,13):        
        if r0[0]['bus'][i,1] == 1:
            ppc          = case14_mod.case14_mod(busN = i,dlt = dlt_vec[j], op_change=1)
            ppopt        = pypo.ppoption(PF_ALG=2, VERBOSE=0, OUT_ALL=0) # Careful: have to use Newton Method!!!
            r            = pypo.runpf(ppc, ppopt)
            #plt.plot(r[0]['bus'][:,2])
            pwr          = r[0]['gen'][:,2][1:] # voltage 7, type 2 
            mtr[tmp,:,j] = pwr
            del(ppc, ppopt, r, pwr)
            tmp += 1
              
## -- plot results
figs = []
axs = []
ims = []

for j in range(0,len(dlt_vec)):
    figs.append(plt.figure(figsize=(10,15)))
    axs.append(figs[j].add_subplot(1,1,1))
    ims.append(axs[j].imshow(100*(mtr[:,:,j]-p0) / p0,
                              interpolation="nearest",
                               cmap="seismic"))
    axs[j].set_title('Powers (Power change: {0})'.format(dlt_vec[j]))
    vname   = 'Power' + str(dlt_vec[j]) + '.png'
    figs[j].colorbar(ims[j],orientation ='horizontal')
    axs[j].set_xlabel('Number of transfomers - generators')
    axs[j].set_ylabel('Load that changed (buildings)')
    figs[j].savefig(os.path.join("../output",vname), dpi=100, clobber=True)   