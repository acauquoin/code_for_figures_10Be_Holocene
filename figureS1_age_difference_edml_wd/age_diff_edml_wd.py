#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# get current directory
cwd = os.getcwd()

# get data
diff_top = pd.read_csv(cwd+'/diff_top.csv', sep=';')
diff_bottom = pd.read_csv(cwd+'/diff_bottom.csv', sep=';')
#
diff_top.set_index('WD2014', inplace=True)
diff_bottom.set_index('WD2014', inplace=True)
#
x=[650, 7350]
y=[0, 0]

# figure
fig, ax = plt.subplots(1,1, figsize=(8, 4), constrained_layout=True)
diff_top.plot(ax=ax, c='tab:red', linewidth=2, legend=False)
diff_bottom.plot(ax=ax, c='tab:red', linewidth=2, legend=False)
ax.plot(x, y, c='k', linewidth=1)

# options of the figures
ax.set_ylabel('Age difference (years)', fontsize=14)
ax.set_xlabel('Age (yr BP)', fontsize=14)
ax.set_xlim(650, 7350)
ax.set_ylim(-19, 19)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_xticks(np.arange(1000, 7001, 500))
ax.set_xticks(np.arange(700, 7301, 100), minor=True)
ax.set_yticks(np.arange(-15, 16, 5))
ax.set_yticks(np.arange(-18, 19, 1), minor=True)
ax.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='k')

# show
plt.show()

# save
fig.savefig(cwd+'/figS1_age_diff_edml_wd.pdf', dpi=300)