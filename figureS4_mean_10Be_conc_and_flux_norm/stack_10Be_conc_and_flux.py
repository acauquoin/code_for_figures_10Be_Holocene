#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# get current directory
cwd = os.getcwd()

# get data
df_stack = pd.read_csv(cwd+'/stack_conc_and_flux.csv', sep=';', na_values=' ')
df_stack.set_index('age_C14', inplace=True)

# figure
fig, ax = plt.subplots(1,1, figsize=(10.83, 4.58), constrained_layout=True)
df_stack.plot(y='stackVK', ax=ax, linewidth=2, label="Concentration")
df_stack.plot(y='stackFluxVK', ax=ax, linewidth=2, c='tab:red', label="Flux")
#
ax.set_xlim(150, 7150)
ax.set_xticks(np.arange(500, 7001, 500))
ax.set_xticks(np.arange(200, 7101, 100), minor=True)
ax.set_ylim(0.78, 1.52)
ax.set_yticks(np.arange(0.8, 1.51, 0.1))
ax.set_yticks(np.arange(0.8, 1.51, 0.05), minor=True)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_ylabel('$^{10}$Be conc. or flux (normalized)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)

# added these three lines
ax.legend(ncol=2, handletextpad=0.5, fontsize=13, columnspacing=1.75, loc='upper center', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/figS4_stack_10Be_conc_and_flux.pdf', dpi=300)

