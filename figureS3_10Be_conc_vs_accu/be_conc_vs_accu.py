#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.tools.eval_measures as smte
import os

# get current directory
cwd = os.getcwd()

# get data
be_conc_accu = pd.read_csv(cwd+'/be_conc_accu_data.csv', sep=';', na_values=' ')
be_conc_accu.accuobs = 1/be_conc_accu.accuobs



# regression equations
# all data
idx_obs = np.isfinite(be_conc_accu.concobs)
t = sm.add_constant(be_conc_accu.accuobs[idx_obs], prepend=False)
model_t_obs = sm.OLS(be_conc_accu.concobs[idx_obs],t)
r_obs = model_t_obs.fit()
p_obs = np.poly1d(r_obs.params)
print((""))
print(("stat conc-accu obs"))
print(("a = {} ± {}".format(r_obs.params.iloc[0], r_obs.bse.iloc[0])))
print(("b = {} ± {}".format(r_obs.params.iloc[1], r_obs.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_obs.conf_int().iloc[0][0], r_obs.conf_int().iloc[0][1])))
print ("r2 = ", r_obs.rsquared)




# figure
fig, ax = plt.subplots(1,1, figsize=(8, 4), constrained_layout=True)
obs = be_conc_accu.plot.scatter(x='accuobs', y='concobs', c='tab:blue', s=60, ax=ax, zorder=200, label=None, alpha=0.5, edgecolors='none')
#
# linear regression plots
ax.plot(be_conc_accu.accuobs[idx_obs], p_obs(be_conc_accu.accuobs[idx_obs]), 'tab:blue', linewidth=2)

#
# annotations of the sites
xpos_beconc_shift = [0.018, 0.018, -0.018, 0.0, 0.02, 0.02, 0.0, 0.0, 0, 0.0, 0]
ypos_beconc_shift = [0, 0, 0, 0.05, 0, 0, -0.06, -0.06, 0.05, -0.06, -0.07]
for i, label in enumerate(be_conc_accu.Site):
    txt = ax.annotate(label, (be_conc_accu.accuobs.iloc[i]+xpos_beconc_shift[i], be_conc_accu.concobs.iloc[i]+ypos_beconc_shift[i]), fontsize=14, color='k', fontweight='bold', horizontalalignment='center', verticalalignment="center", zorder=600)
#
# equations
ax.text(0.28, 0., r'{:.3f}'.format(r_obs.params.iloc[0])+'$\mathbf{\cdot10^5}$ at.cm$\mathbf{^{-2}}$.yr$\mathbf{^{-1}}$'+'; $\mathbf{r^2}$ = '+'{:.2f}'.format(r_obs.rsquared), color='tab:blue', fontsize=12, fontweight='semibold')

# options of the figures
ax.set_xlabel('1/accumulation (1 / (g.cm$^{-2}$.yr$^{-1}$))', fontsize=14)
ax.set_ylabel('$^{10}$Be concentration (10$^5$ at.g$^{-1}$)', fontsize=14)
ax.set_xlim(0.01, 0.49)
ax.set_ylim(-0.05, 1.05)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_xticks(np.arange(0.05, 0.46, 0.05))
ax.set_xticks(np.arange(0.025, 0.48, 0.025), minor=True)
ax.set_yticks(np.arange(0, 1.1, 0.2))
ax.set_yticks(np.arange(0, 1.1, 0.1), minor=True)

# show
plt.show()

# save
fig.savefig(cwd+'/figS3_10Be_conc_vs_accu.pdf', dpi=300)