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
be_conc_elev = pd.read_csv(cwd+'/be_conc_altitude_data_model.csv', sep=';', na_values=' ')
be_jra59 = pd.read_csv(cwd+'/JARE59_conc_elev.csv', sep=';', na_values=' ')



# regression equations
idx_obs = np.isfinite(be_conc_elev.concobs)
t = sm.add_constant(be_conc_elev.zobs[idx_obs], prepend=False)
model_t_obs = sm.OLS(be_conc_elev.concobs[idx_obs],t)
r_obs = model_t_obs.fit()
p_obs = np.poly1d(r_obs.params)
print((""))
print(("stat alt-conc obs"))
print(("a = {} ± {}".format(r_obs.params.iloc[0], r_obs.bse.iloc[0])))
print(("b = {} ± {}".format(r_obs.params.iloc[1], r_obs.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_obs.conf_int().iloc[0][0], r_obs.conf_int().iloc[0][1])))
print ("r2 = ", r_obs.rsquared)
#
idx_mod = np.isfinite(be_conc_elev.concmod)
t = sm.add_constant(be_conc_elev.zmod[idx_mod], prepend=False)
model_t_mod = sm.OLS(be_conc_elev.concmod[idx_mod],t)
r_mod = model_t_mod.fit()
p_mod = np.poly1d(r_mod.params)
print((""))
print(("stat alt-conc model"))
print(("a = {} ± {}".format(r_mod.params.iloc[0], r_mod.bse.iloc[0])))
print(("b = {} ± {}".format(r_mod.params.iloc[1], r_mod.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_mod.conf_int().iloc[0][0], r_mod.conf_int().iloc[0][1])))
print ("r2 = ", r_mod.rsquared)
#
idx_above3500 = be_jra59.Elevation > 3500
t = sm.add_constant(be_jra59.Elevation[idx_above3500], prepend=False)
model_t_jare_above3500 = sm.OLS(be_jra59["10Be_conc"][idx_above3500],t)
r_jare_above3500 = model_t_jare_above3500.fit()
p_jare_above3500 = np.poly1d(r_jare_above3500.params)
print((""))
print(("stat alt-conc JARE59 above 3500m"))
print(("a = {} ± {}".format(r_jare_above3500.params.iloc[0], r_jare_above3500.bse.iloc[0])))
print(("b = {} ± {}".format(r_jare_above3500.params.iloc[1], r_jare_above3500.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_jare_above3500.conf_int().iloc[0][0], r_jare_above3500.conf_int().iloc[0][1])))
print ("r2 = ", r_jare_above3500.rsquared)
#
idx_below3500 = be_jra59.Elevation < 3500
t = sm.add_constant(be_jra59.Elevation[idx_below3500], prepend=False)
model_t_jare_below3500 = sm.OLS(be_jra59["10Be_conc"][idx_below3500],t)
r_jare_below3500 = model_t_jare_below3500.fit()
p_jare_below3500 = np.poly1d(r_jare_below3500.params)
print((""))
print(("stat alt-conc JARE59 below 3500m"))
print(("a = {} ± {}".format(r_jare_below3500.params.iloc[0], r_jare_below3500.bse.iloc[0])))
print(("b = {} ± {}".format(r_jare_below3500.params.iloc[1], r_jare_below3500.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_jare_below3500.conf_int().iloc[0][0], r_jare_below3500.conf_int().iloc[0][1])))
print ("r2 = ", r_jare_below3500.rsquared)
#
idx_east = be_conc_elev.Longitude > 0
t = sm.add_constant(be_conc_elev.zobs[idx_east], prepend=False)
model_t_obs_east = sm.OLS(be_conc_elev.concobs[idx_east],t)
r_obs_east = model_t_obs_east.fit()
p_obs_east = np.poly1d(r_obs_east.params)
print((""))
print(("stat alt-conc obs east"))
print(("a = {} ± {}".format(r_obs_east.params.iloc[0], r_obs_east.bse.iloc[0])))
print(("b = {} ± {}".format(r_obs_east.params.iloc[1], r_obs_east.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_obs_east.conf_int().iloc[0][0], r_obs_east.conf_int().iloc[0][1])))
print ("r2 = ", r_obs_east.rsquared)
#
t = sm.add_constant(be_conc_elev.zmod[idx_east], prepend=False)
model_t_mod_east = sm.OLS(be_conc_elev.concmod[idx_east],t)
r_mod_east = model_t_mod_east.fit()
p_mod_east = np.poly1d(r_mod_east.params)
print((""))
print(("stat alt-conc mod east"))
print(("a = {} ± {}".format(r_mod_east.params.iloc[0], r_mod_east.bse.iloc[0])))
print(("b = {} ± {}".format(r_mod_east.params.iloc[1], r_mod_east.bse.iloc[1])))
print (("95% confidence interval = [ {} ; {} ]".format(r_mod_east.conf_int().iloc[0][0], r_mod_east.conf_int().iloc[0][1])))
print ("r2 = ", r_mod_east.rsquared)



# figure
fig, ax = plt.subplots(1,1, figsize=(8, 4), constrained_layout=True)
obs = be_conc_elev.plot.scatter(x='zobs', y='concobs', c='tab:blue', s=60, ax=ax, zorder=200, label="Observations", alpha=0.5, edgecolors='none')
mod = be_conc_elev.plot.scatter(x='zmod', y='concmod', c='tab:red', s=60, ax=ax, zorder=200, label="ECHAM6.3-HAM2.3", alpha=0.5, edgecolors='none')
jare = be_jra59.plot.scatter(x='Elevation', y='10Be_conc', c='tab:olive', s=60, ax=ax, zorder=200, label="JARE59 observational dataset", alpha=0.5, edgecolors='none')
#
# scatter plots
ax.plot(be_conc_elev.zobs[idx_obs], p_obs(be_conc_elev.zobs[idx_obs]), 'tab:blue', linewidth=2)
ax.plot(be_conc_elev.zmod[idx_mod], p_mod(be_conc_elev.zmod[idx_mod]), 'tab:red', linewidth=2)
ax.plot(be_jra59.Elevation[idx_above3500], p_jare_above3500(be_jra59.Elevation[idx_above3500]), 'darkolivegreen', linewidth=2)
ax.plot(be_jra59.Elevation[idx_below3500], p_jare_below3500(be_jra59.Elevation[idx_below3500]), 'yellowgreen', linewidth=2)
ax.plot(be_conc_elev.zobs[idx_east], p_obs_east(be_conc_elev.zobs[idx_east]), 'navy', linewidth=2)
#
# line between modeled and observed values for the same site
for i in range(be_conc_elev.shape[0]):
    a, b, c, d = zip(be_conc_elev.iloc[i, 3:])
    ax.plot([a, c], [b, d], c='black')
#
# annotations of the sites
xpos_beconc_shift = [0, 150, -200, 320, 0, 200, 130, -160, 0, 110, 0]
ypos_beconc_shift = [0.05, 0, -0.032, -0.06, 0.1, 0, -0.04, 0, 0.15, 0, -0.05]
for i, label in enumerate(be_conc_elev.Site):
    txt = ax.annotate(label, (np.mean([be_conc_elev.zobs.iloc[i], be_conc_elev.zmod.iloc[i]])+xpos_beconc_shift[i], np.mean([be_conc_elev.concobs.iloc[i], be_conc_elev.concmod.iloc[i]])+ypos_beconc_shift[i]), fontsize=14, color='k', fontweight='bold', horizontalalignment='center', verticalalignment="center", zorder=600)
#
# equations
ax.text(-125, 0.72, r'{:.3f}'.format(r_obs.params.iloc[0]*1000.)+'$\mathbf{\cdot10^5}$ at.g$\mathbf{^{-1}}$.km$\mathbf{^{-1}}$'+'; $\mathbf{r^2}$ = '+'{:.2f}'.format(r_obs.rsquared), color='tab:blue', fontsize=12, fontweight='semibold')
ax.text(-125, 0.65, r'{:.3f}'.format(r_mod.params.iloc[0]*1000.)+'$\mathbf{\cdot10^5}$ at.g$\mathbf{^{-1}}$.km$\mathbf{^{-1}}$'+'; $\mathbf{r^2}$ = '+'{:.2f}'.format(r_mod.rsquared), color='tab:red', fontsize=12, fontweight='semibold')
ax.text(-125, 0.58, r'{:.3f}'.format(r_obs_east.params.iloc[0]*1000.)+'$\mathbf{\cdot10^5}$ at.g$\mathbf{^{-1}}$.km$\mathbf{^{-1}}$'+'; $\mathbf{r^2}$ = '+'{:.2f}'.format(r_obs_east.rsquared), color='navy', fontsize=12, fontweight='semibold')
ax.text(-125, 0.51, r'{:.3f}'.format(r_jare_above3500.params.iloc[0]*1000.)+'$\mathbf{\cdot10^5}$ at.g$\mathbf{^{-1}}$.km$\mathbf{^{-1}}$'+'; $\mathbf{r^2}$ = '+'{:.2f}'.format(r_jare_above3500.rsquared), color='darkolivegreen', fontsize=12, fontweight='semibold')
ax.text(-125, 0.44, r'{:.3f}'.format(r_jare_below3500.params.iloc[0]*1000.)+'$\mathbf{\cdot10^5}$ at.g$\mathbf{^{-1}}$.km$\mathbf{^{-1}}$'+'; $\mathbf{r^2}$ = '+'{:.2f}'.format(r_jare_below3500.rsquared), color='yellowgreen', fontsize=12, fontweight='semibold')
# options of the figures
ax.set_xlabel('Altitude (m)', fontsize=14)
ax.set_ylabel('$^{10}$Be concentration (10$^5$ at.g$^{-1}$)', fontsize=14)
ax.set_xlim(-200, 4200)
ax.set_ylim(-0.05, 1.05)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_xticks(np.arange(0, 4001, 500))
ax.set_xticks(np.arange(-100, 4101, 100), minor=True)
ax.set_yticks(np.arange(0, 1.1, 0.2))
ax.set_yticks(np.arange(0, 1.1, 0.1), minor=True)
#
# Legend
ax.legend(ncol=1, handletextpad=0.2, fontsize=12, loc='upper left', borderaxespad=0.2, borderpad=0.4, alignment="left", labelspacing=0.6, scatteryoffsets=[0.5], frameon=False, bbox_to_anchor=(-0.01, 1))

# show
plt.show()

# save
fig.savefig(cwd+'/fig08_10Be_conc_vs_altitude.pdf', dpi=300)