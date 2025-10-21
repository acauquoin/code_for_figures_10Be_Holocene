#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# get current directory
cwd = os.getcwd()

# get data
df_c14 = pd.read_csv(cwd+'/sim_c14_time_series.csv', sep=';', na_values=' ')
df_c14.set_index('age', inplace=True)

# figure
fig, ax = plt.subplots(1,1, figsize=(10.83, 4.58), constrained_layout=True)
df_c14['stackVKtr'].plot(ax=ax, label='conc.', c='k', linewidth=2)
df_c14['stackVKtr_pm8percent'].plot(ax=ax, label='conc. ± 8 %', c='tab:blue', linewidth=2)
df_c14['stackVKtr_pm12percent'].plot(ax=ax, label='conc. ± 12 %', c='tab:orange', linewidth=2)
df_c14['Mean_conc_plus_trend1.35'].plot(ax=ax, label=r'conc. + adjustments', c='tab:olive', linewidth=2)
#
ax.set_xlim(150, 7150)
ax.set_xticks(np.arange(500, 7001, 500))
ax.set_xticks(np.arange(200, 7101, 100), minor=True)
ax.set_ylim(-24, 44)
ax.set_yticks(np.arange(-20, 41, 10))
ax.set_yticks(np.arange(-20, 41, 5), minor=True)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_ylabel('$\Delta^{14}$C based on $^{10}$Be conc (‰)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)

# added these three lines
#lines, labels = ax.get_legend_handles_labels()
#lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(ncol=1, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='lower right', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/fig09_sim_c14_time_series.pdf', dpi=300)

