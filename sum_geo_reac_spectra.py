import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

filename = sys.argv[1]

u = 1.6605402e-27 # kg
m_o = 15.999*u
m_h = 1*u
m_water = 2*m_h+m_o
m_sk = 22.5e6 # kg (FV)
n_water_sk = m_sk/m_water
n_p_sk = n_water_sk*2

# 1 TNU = 1 event/10e32 protons/year

print("N free protons in SK = %g\n" % n_p_sk)

geo_file = pd.read_csv(filename, 
    header=None,
    names=["tot",
        "standard_reactors",
        "closest",
        "custom",
        "U",
        "Th"]
    )

bin_width = (geo_file.index[1]-geo_file.index[0])*1000 # E is in MeV, not keV
print("Bin width = %f" % bin_width)

scale = bin_width*n_p_sk/1e32

geo_file = geo_file.apply(lambda x: x*scale)

print("N interactions = %f" % geo_file["standard_reactors"].sum())

geo_file["standard_reactors"].plot()
plt.show()