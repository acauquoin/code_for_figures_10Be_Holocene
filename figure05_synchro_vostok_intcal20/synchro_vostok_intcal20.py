#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# get current directory
cwd = os.getcwd()

# get data
Be_vostok = pd.read_csv(cwd+'/Be_vostok.csv', sep=';', na_values=' ')
intcal20 = pd.read_csv(cwd+'/intcal20_detrended_norm.csv', sep=';', na_values=' ')
d18o_vostok = pd.read_csv(cwd+'/d18o_vostok.csv', sep=';', na_values=' ')
C14Be_aicc = pd.read_csv(cwd+'/C14Be_aicc.csv', sep=';', na_values=' ')
C14Be_synchro = pd.read_csv(cwd+'/C14Be_synchro.csv', sep=';', na_values=' ')
#
Be_vostok.set_index('AICCBeNorm', inplace=True)
intcal20.set_index('AgeC14intcal', inplace=True)
d18o_vostok.set_index('AICCoxy', inplace=True)
C14Be_aicc.set_index('AICC-C14Be', inplace=True)
C14Be_synchro.set_index('Age_synchroBe', inplace=True)

# figure
fig, axs = plt.subplots(3,1, sharex=True, figsize=(8, 8.66), constrained_layout=True)
d18o_vostok.plot(ax=axs[0], xlim=(0,8000), ylim=(-58.5,-54.5), c='grey', legend=False)
Be_vostok.plot(ax=axs[1], xlim=(0,8000), ylim=(-4.5, 4.5), c='tab:blue')
C14Be_aicc.plot(ax=axs[1], xlim=(0,8000), ylim=(-4.5, 4.5), c='tab:red')
intcal20.plot(ax=axs[2], xlim=(0,8000), ylim=(-4.5, 4.5), c='k')
C14Be_synchro.plot(ax=axs[2], xlim=(0,8000), ylim=(-4.5, 4.5), c='tab:red')
 
# options of the figures
axs[0].set_ylabel('$\mathsf{\delta^{18}O}$ (‰)', fontsize=14)
axs[1].set_ylabel('Norm. $\Delta^{14}$C or $^{10}$Be conc.', fontsize=14)
axs[2].set_ylabel('Norm. $\Delta^{14}$C or $^{10}$Be conc.', fontsize=14)
axs[2].set_xlabel('')
string = ['(a)', '(b)', '(c)']
i=0
for ax in np.ravel(axs):
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_xticks(np.arange(1000, 7001, 2000))
    ax.set_xticks(np.arange(0, 8001, 500), minor=True)
    ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
    ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
    ax.text(0.004, 0.985, string[i], fontsize=14, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
    i=i+1

# Legend
axs[1].legend(['$^{10}$Be Vostok (AICC)', '$\Delta^{14}$C derived $^{10}$Be Vostok (AICC)'], ncol=2, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='lower right', borderaxespad=0.3)
axs[2].legend(['Detrended $\Delta^{14}$C IntCal20', '$\Delta^{14}$C derived $^{10}$Be Vostok (redated)'], ncol=2, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='lower right', borderaxespad=0.3)
#
fig.supxlabel('Age (yr BP)', fontsize=14, x=0.54)
fig.align_ylabels()

# show
plt.show()

# save
fig.savefig(cwd+'/fig05_synchro_vostok_intcal20.pdf', dpi=300)