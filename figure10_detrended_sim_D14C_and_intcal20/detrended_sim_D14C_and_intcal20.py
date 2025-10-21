#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy import stats
from scipy.stats import linregress, kendalltau
import os

# get current directory
cwd = os.getcwd()

# Z-test function for dependant correlations
def compare_dependent_correlations(r12, r13, r23, n):
    """
    Performs Steiger's z-test for the difference between two dependent correlations.

    Args:
        r12 (float): Correlation between variable 1 and 2.
        r13 (float): Correlation between variable 1 and 3.
        r23 (float): Correlation between variable 2 and 3.
        n (int): The sample size.

    Returns:
        tuple: A tuple containing the z-statistic and the two-tailed p-value.
    """
    # Denominator is 2 times the determinant of the correlation matrix
    determinant = 1 - r12**2 - r13**2 - r23**2 + (2 * r12 * r13 * r23)
    
    # Calculate the z-statistic
    z_stat = (r12 - r13) * np.sqrt(((n - 3) * (1 + r23)) / (2 * determinant))
    
    # Calculate the two-tailed p-value from the standard normal distribution
    p_value = 2 * stats.norm.sf(np.abs(z_stat))
    
    return z_stat, p_value

# get data
intcal20 = pd.read_csv(cwd+'/intcal20_detrended.csv', sep=';', na_values=' ')
sim_C14Be = pd.read_csv(cwd+'/sim_C14_detrended.csv', sep=';', na_values=' ')

# interpolate on the same age scale to calculate the linear regression correlation
interp_func = interp1d(intcal20['age'], intcal20['intcal20_detrended'], kind='linear')
C14_intcal20_interp = interp_func(sim_C14Be['age'])
reg_stack = linregress(C14_intcal20_interp, sim_C14Be["C14_mean_stack"])
ktau_stack = kendalltau(C14_intcal20_interp, sim_C14Be["C14_mean_stack"])
print ('Stack:')
print ('------')
print ('r value = ', f'{reg_stack.rvalue:.4f}', ', p-value = ', f'{reg_stack.pvalue:.4e}')
print('kendall tau = ', f'{ktau_stack.statistic:.4f}', ', p-value = ', f'{ktau_stack.pvalue:.4e}')
print('')
reg_vostok = linregress(C14_intcal20_interp, sim_C14Be["C14_vostok"])
ktau_vostok = kendalltau(C14_intcal20_interp, sim_C14Be["C14_vostok"])
print ('Vostok:')
print ('-------')
print ('r value = ', f'{reg_vostok.rvalue:.4f}', ', p-value = ', f'{reg_vostok.pvalue:.4e}')
print('kendall tau = ', f'{ktau_vostok.statistic:.4f}', ', p-value = ', f'{ktau_vostok.pvalue:.4e}')
print('')

# test if the 2 correlations are significantly different
# Correlation between Intcal20 and C14_mean_stack
r12 = reg_stack.rvalue
# orrelation between Intcal20 and C14_vostok
r13 = reg_vostok.rvalue
# We also need the correlation between C14_mean_stack and C14_vostok
reg_sim = linregress(sim_C14Be["C14_mean_stack"], sim_C14Be["C14_vostok"])
r23 = reg_sim.rvalue
# Sample size
n = len(C14_intcal20_interp)

# Perform the z-test
z_statistic, p_value = compare_dependent_correlations(r12, r13, r23, n)
print('Difference between the two correlations:')
print('----------------------------------------')
print(f"Z-statistic: {z_statistic:.4f}")
print(f"P-value: {p_value:.4e}")

# --- Interpretation ---
alpha = 0.05
if p_value < alpha:
    print("The difference between the two correlations is statistically significant.")
else:
    print("The difference between the two correlations is not statistically significant.")

# restrict values for plotting
intcal20.set_index('age', inplace=True)
sim_C14Be.set_index('age', inplace=True)
intcal20 = intcal20.loc[240:7100]

# figure v1 (two subplots)
fig, axs = plt.subplots(2,1, sharex=True, figsize=(12.68,  6.72), constrained_layout=True)
intcal20["intcal20_detrended"].plot(ax=axs[0], xlim=(0,8000), ylim=(-22, 22), c='k', label='IntCal20', linewidth=2)
sim_C14Be["C14_mean_stack"].plot(ax=axs[0], xlim=(150, 7150), ylim=(-22, 22), c='tab:red', label='Stack', linewidth=2)
intcal20["intcal20_detrended"].plot(ax=axs[1], xlim=(150, 7150), ylim=(-22, 22), c='k', label='', linewidth=2)
sim_C14Be["C14_vostok"].plot(ax=axs[1], xlim=(150, 7150), ylim=(-22, 22), c='dodgerblue', label='Vostok', linewidth=2)
 #
# options of the figures
axs[1].set_xlabel('')
for ax in np.ravel(axs):
    ax.set_ylabel('', fontsize=14)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_xticks(np.arange(500, 7001, 500))
    ax.set_xticks(np.arange(200, 7101, 100), minor=True)
    ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
    ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
#
# Legend
leg = fig.legend(loc='outside upper right', ncol=3, handletextpad=0.5, fontsize=12, columnspacing=1.75, borderaxespad=0.3)
#
fig.supylabel('Detrended $\Delta^{14}$C (‰)', fontsize=14, y=0.515)
fig.supxlabel('Age (yr BP)', fontsize=14, x=0.53)
fig.align_ylabels()
#
# show
plt.show()
#
# save
fig.savefig(cwd+'/fig10_detrended_sim_D14C_and_intcal20_2subplots.pdf', dpi=300)


# figure v2 (one subplot)
fig, ax = plt.subplots(1,1, sharex=True, figsize=(12.68, 3.5), constrained_layout=True)
intcal20["intcal20_detrended"].plot(ax=ax, xlim=(150, 7150), ylim=(-22, 22), c='k', label='IntCal20', linewidth=2)
sim_C14Be["C14_mean_stack"].plot(ax=ax, xlim=(150, 7150), ylim=(-22, 22), c='tab:red', label='Stack', linewidth=2)
sim_C14Be["C14_vostok"].plot(ax=ax, xlim=(150, 7150), ylim=(-22, 22), c='dodgerblue', label='Vostok', linewidth=2)
#
# options of the figures
ax.set_ylabel('Detrended $\Delta^{14}$C (‰)', fontsize=14)
ax.set_xlabel('Age (yr BP)', fontsize=14)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
ax.set_xticks(np.arange(500, 7001, 500))
ax.set_xticks(np.arange(200, 7101, 100), minor=True)
ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='k')
ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='darkgrey')
#
# Legend
leg = ax.legend(loc='lower right', ncol=3, handletextpad=0.5, fontsize=12, columnspacing=1.75, borderaxespad=0.3)
#
# show
plt.show()
#
# save
fig.savefig(cwd+'/fig10_detrended_sim_D14C_and_intcal20_1subplot.pdf', dpi=300)