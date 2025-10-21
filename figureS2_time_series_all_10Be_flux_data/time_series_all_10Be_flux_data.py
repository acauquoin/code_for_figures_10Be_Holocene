#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os
import colormaps as cmaps


# get current directory
cwd = os.getcwd()

# get data
flux = pd.read_csv(cwd+'/synchronized_time_series_all_10Be_flux_data.csv', sep=';', na_values=' ')
flux.set_index('age_synchro', inplace=True)
flux.columns = flux.columns.str.replace('Flux','')
#
cmap = cmaps.tableau_10  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list
fig, ax = plt.subplots(1,1, sharex=True, figsize=(8, 6.2), constrained_layout=True)
ax.set_prop_cycle(color=colors)
for series_name, series in flux.items():
    if series_name == 'VK':
        flux.plot(y=series_name, ax=ax, c='k')
    else:
        flux.plot(y=series_name, ax=ax)
ax.set_xlim(-50, 7250)
ax.set_ylim(15, 215)
ax.set_ylabel('$^{10}$Be flux (at.m$^{-2}$.s$^{-1}$)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)

# legend
ax.legend(ncol=3, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='upper left', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/figS2_all_10Be_flux_data_time_series.pdf', dpi=300)

