#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# get current directory
cwd = os.getcwd()

# get data
df_stack = pd.read_csv(cwd+'/calcul_stack_vostok_10Beconc.csv', sep=';', na_values=' ')
df_stack.set_index('age_C14', inplace=True)
vostok = df_stack.BeVKn
other = df_stack.iloc[:,1:11]
stack = df_stack.stackVK
num_sites = df_stack.number_sites

# set Column names, to hide labels in legend for the other time series
cols = ["_" + col for col in other.columns]
cols[0] = 'Other sites'
other.columns = cols

# figure
fig, ax = plt.subplots(1,1, figsize=(10.83, 4.58), constrained_layout=True)
ax2 = ax.twinx()
num_sites.plot(ax=ax2, label='Number of sites', c='tab:blue')
other.plot(ax=ax, c='grey', linewidth=0.75)
vostok.plot(ax=ax, label='Vostok', c='tab:red', linewidth=2)
stack.plot(ax=ax, label='Stack', c='k', linewidth=2)
#
ax.set_xlim(150, 7150)
ax.set_xticks(np.arange(500, 7001, 500))
ax.set_xticks(np.arange(200, 7101, 100), minor=True)
ax.set_ylim(0.55, 1.65)
ax.set_yticks(np.arange(0.6, 1.61, 0.2))
ax.set_yticks(np.arange(0.6, 1.61, 0.1), minor=True)
ax2.set_ylim(0.8, 9.2)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax2.yaxis.set_tick_params(labelsize=12)
ax.set_ylabel('$^{10}$Be concentration (normalized)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)
ax2.set_ylabel('Number of sites', fontsize=16, rotation=270, labelpad=23)

# added these three lines
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines+lines2, labels+labels2, ncol=2, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='upper center', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/fig09_stack_vostok_10Beconc_time_series.pdf', dpi=300)

