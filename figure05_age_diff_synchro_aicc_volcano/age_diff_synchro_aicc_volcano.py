#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# get current directory
cwd = os.getcwd()

# get data
diff_synchro = pd.read_csv(cwd+'/age_diff_synchro_aicc_volcano.csv', sep=';', na_values=' ')
diff_synchro.set_index('Age Synchro C14', inplace=True)
x=[-200, 7500]
y=[0, 0]

# figure
fig, ax = plt.subplots(1,1, figsize=(8, 4), constrained_layout=True)
ax.plot(x, y, c='k', linewidth=1)
aicc, = ax.plot(diff_synchro['Diff AICC'], c='tab:blue', linewidth=2)
volcwd, = ax.plot(diff_synchro['Diff volcanoWD'], c='tab:orange', linewidth=2)
volcsp, = ax.plot(diff_synchro['Diff volcanoPS1'], c='saddlebrown', linewidth=2)

# options of the figures
ax.set_ylabel('Age difference (years)', fontsize=14)
ax.set_xlabel('Age (yr BP)', fontsize=14)
ax.set_xlim(-200, 7200)
ax.set_ylim(-78, 58)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_xticks(np.arange(0, 7001, 1000))
ax.set_xticks(np.arange(500, 7001, 500), minor=True)
ax.set_yticks(np.arange(-60, 41, 20))
ax.set_yticks(np.arange(-70, 51, 10), minor=True)
ax.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='k')

# Legend
ax.legend([aicc, volcwd, volcsp], ['$^{14}$C age $-$ AICC', '$^{14}$C age $-$ $^{10}$Be VolcanoWD', '$^{14}$C age $-$ $^{10}$Be VolcanoPS1'],  ncol=1, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='upper right', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/fig05_age_diff_synchro_aicc_volcano.pdf', dpi=300)