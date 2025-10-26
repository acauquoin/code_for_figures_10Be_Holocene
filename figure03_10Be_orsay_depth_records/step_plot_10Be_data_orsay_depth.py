#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os

# get current directory
cwd = os.getcwd()

# get data
BH1 = pd.read_csv(cwd+'/BH1.csv', sep=';', na_values=' ')
BH2 = pd.read_csv(cwd+'/BH2.csv', sep=';', na_values=' ')
domeA = pd.read_csv(cwd+'/DomeA.csv', sep=';', na_values=' ')
EDC = pd.read_csv(cwd+'/EDC.csv', sep=';', na_values=' ')
ODC = pd.read_csv(cwd+'/ODC.csv', sep=';', na_values=' ')
SP = pd.read_csv(cwd+'/SP.csv', sep=';', na_values=' ')
#
BH1.set_index('depth', inplace=True)
BH2.set_index('depth', inplace=True)
domeA.set_index('depth', inplace=True)
EDC.set_index('depth', inplace=True)
ODC.set_index('depth', inplace=True)
SP.set_index('depth', inplace=True)

# figure
fig, axs = plt.subplots(4,1, sharex=True, figsize=(8, 6.2), constrained_layout=True)

axs[0].plot(BH1,   drawstyle='steps-post', c='red', label='Vostok BH1')
axs[0].plot(BH2,   drawstyle='steps-post', c='orange', label='Vostok BH2')
axs[1].plot(domeA, drawstyle='steps-post', c='tab:green', label='Dome A')
axs[2].plot(SP,    drawstyle='steps-post', c='brown', label='South Pole')
axs[3].plot(EDC,   drawstyle='steps-post', c='k', label='EPICA Dome C')
axs[3].plot(ODC,   drawstyle='steps-post', c='grey', label='Old Dome C')

# options of the figure
#axs[0].spines[['bottom']].set_visible(False)
axs[0].set_xlim(-1,179)
axs[0].set_xticks(np.arange(10,171,20))
axs[0].set_xticks(np.arange(5,180,5), minor=True)
axs[0].tick_params(bottom=False, which='both')
axs[0].grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
axs[0].grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
ymax = math.ceil(np.max(BH1) * 10) / 10
ymin = math.floor(np.min(BH2) * 10) / 10
axs[0].set_ylim(ymin, ymax)
axs[0].set_yticks(np.linspace(ymin+0.1, ymax-0.1, 3))
axs[0].text(100, ymin+0.05, 'Vostok BH1', color='red', fontsize=14, fontweight='demibold')
axs[0].text(20, ymin+0.05, 'Vostok BH2', color='orange', fontsize=14, fontweight='demibold')
axs[0].text(0.002, 0.985, '(a)', fontsize=14, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=axs[0].transAxes)
#axs[1].spines[['top', 'bottom']].set_visible(False)
axs[1].tick_params(bottom=False, which='both')
axs[1].grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
axs[1].grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
ymax = math.ceil(np.max(domeA) * 10) / 10
ymin = math.floor(np.min(domeA) * 10) / 10
axs[1].set_ylim(ymin, ymax)
axs[1].set_yticks(np.linspace(ymin+0.1, ymax-0.1, 3))
axs[1].text(112, ymin+0.05, 'Dome A', color='tab:green', fontsize=14, fontweight='demibold')
axs[1].text(0.002, 0.985, '(b)', fontsize=14, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=axs[1].transAxes)
#axs[1].yaxis.tick_right()
#axs[1].yaxis.set_label_position("right")
#axs[2].spines[['top', 'bottom']].set_visible(False)
axs[2].tick_params(bottom=False, which='both')
axs[2].grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
axs[2].grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
ymax = math.ceil(np.max(SP) * 10) / 10
ymin = math.floor(np.min(SP) * 10) / 10
axs[2].set_ylim(ymin, ymax)
axs[2].set_yticks(np.linspace(ymin+0.05, ymax-0.05, 3))
axs[2].text(128, ymin+0.025, 'PS1', color='brown', fontsize=14, fontweight='demibold')
axs[2].text(0.002, 0.985, '(c)', fontsize=14, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=axs[2].transAxes)
#axs[3].spines[['top']].set_visible(False)
#axs[3].yaxis.tick_right()
#axs[3].yaxis.set_label_position("right")
axs[3].grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
axs[3].grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
ymax = math.ceil(np.max(EDC) * 10) / 10
ymin = math.floor(np.min(ODC) * 10) / 10
axs[3].set_ylim(ymin, ymax)
axs[3].set_yticks(np.linspace(ymin+0.1, ymax-0.1, 3))
axs[3].text(10, ymin+0.05, 'EPICA Dome C', color='k', fontsize=14, fontweight='demibold')
axs[3].text(100, 0.7, 'Old Dome C', color='grey', fontsize=14, fontweight='demibold')
axs[3].text(0.002, 0.985, '(d)', fontsize=14, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=axs[3].transAxes)
#
fig.supylabel('$^{10}$Be concentration (10$^5$ at/g)', fontsize=16, y=0.535)
fig.supxlabel('Depth (m)', fontsize=16, x=0.54)

# show
plt.show()

# save
fig.savefig(cwd+'/fig03_10Be_data_orsay_depth.pdf', dpi=300)

