#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# get current directory
cwd = os.getcwd()

# get data
df_stack = pd.read_csv(cwd+'/sim_C14_from_stack_conc_and_flux.csv', sep=';', na_values=' ')
df_stack.set_index('age', inplace=True)

# figure
fig, ax = plt.subplots(1,1, figsize=(10.83, 4.58), constrained_layout=True)
df_stack.plot(y='stackVKtr', ax=ax, linewidth=2, label="Concentration")
df_stack.plot(y='stackFluxVKtr', ax=ax, linewidth=2, c='tab:red', label="Flux")
#
ax.set_xlim(150, 7150)
ax.set_xticks(np.arange(500, 7001, 500))
ax.set_xticks(np.arange(200, 7101, 100), minor=True)
ax.set_ylim(-19, 39)
ax.set_yticks(np.arange(-15, 36, 10))
ax.set_yticks(np.arange(-15, 36, 5), minor=True)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_ylabel('$\Delta^{14}$C (‰)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)

# added these three lines
ax.legend(ncol=2, handletextpad=0.5, fontsize=13, columnspacing=1.75, loc='upper left', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/figS6_sim_D14C_from_conc_and_flux.pdf', dpi=300)

