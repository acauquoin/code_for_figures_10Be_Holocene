#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import os


# get current directory
cwd = os.getcwd()

# get data
df_stack = pd.read_csv(cwd+'/calcul_stack_SP_10Beconc.csv', sep=';', na_values=' ')
df_stack.set_index('AgeSPs', inplace=True)
sp = df_stack['BeSPnorm']
other = df_stack.iloc[:,1:9]
stack = df_stack['stack']

# set Column names, to hide labels in legend for the other time series
cols = ["_" + col for col in other.columns]
cols[0] = 'Other sites'
other.columns = cols

# figure
fig, ax = plt.subplots(1,1, figsize=(10.83, 4.58), constrained_layout=True)
other.plot(ax=ax, c='grey', linewidth=0.75)
sp.plot(ax=ax, label='PS1', c='tab:red', linewidth=2)
stack.plot(ax=ax, label='Stack', c='k', linewidth=2)
#
ax.set_xlim(-40, 1140)
ax.set_xticks(np.arange(0, 1101, 100))
ax.set_xticks(np.arange(0, 1101, 50), minor=True)
ax.set_ylim(0.65, 1.55)
ax.set_yticks(np.arange(0.7, 1.51, 0.1))
#
ax2 = ax.twiny()
ax2.set_xticks(ax.get_xticks())
ax2.set_xbound(ax.get_xbound())
ax2.set_xticklabels([(1950-x) for x in ax.get_xticks()])
ax2.xaxis.set_minor_locator(AutoMinorLocator(2))
#
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_ylabel('$^{10}$Be concentration (normalized)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)
ax2.xaxis.set_tick_params(labelsize=12)
ax2.set_xlabel('Age (yr CE)', fontsize=16, labelpad=7)

# legend
lines, labels = ax.get_legend_handles_labels()
ax.legend(ncol=3, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='upper right', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/figS5_stack_SP_10Beconc_time_series.pdf', dpi=300)

