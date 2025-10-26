#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os
import colormaps as cmaps


# get current directory
cwd = os.getcwd()

# get data
vostok = pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_vostok', 'Be_conc_vostok'])
DA =     pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_da',     'Be_conc_da']    )
EDC =    pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_edc',    'Be_conc_edc']   )
ODC =    pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_odc',    'Be_conc_odc']   )
SP =     pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_sp',     'Be_conc_sp']    )
DF =     pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_df',     'Be_conc_df']    )
EDML =   pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_edml',   'Be_conc_edml']  )
LDC =    pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_ldc',    'Be_conc_ldc']   )
SD =     pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_sd',     'Be_conc_sd']    )
SPI =    pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_spi',    'Be_conc_spi']   )
TD =     pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_td',     'Be_conc_td']    )
WD =     pd.read_csv(cwd+'/time_series_all_10Be_conc_data.csv', sep=';', na_values=' ', usecols=['age_wd',     'Be_conc_wd']    )
#
vostok.set_index('age_vostok', inplace=True)
DA.set_index('age_da', inplace=True)
EDC.set_index('age_edc', inplace=True)
ODC.set_index('age_odc', inplace=True)
SP.set_index('age_sp', inplace=True)
DF.set_index('age_df', inplace=True)
EDML.set_index('age_edml', inplace=True)
LDC.set_index('age_ldc', inplace=True)
SD.set_index('age_sd', inplace=True)
SPI.set_index('age_spi', inplace=True)
TD.set_index('age_td', inplace=True)
WD.set_index('age_wd', inplace=True)
#
DA = DA.loc[DA.index.dropna()]
EDC = EDC.loc[EDC.index.dropna()]
ODC = ODC.loc[ODC.index.dropna()]
SP = SP.loc[SP.index.dropna()]
DF = DF.loc[DF.index.dropna()]
EDML = EDML.loc[EDML.index.dropna()]
LDC = LDC.loc[LDC.index.dropna()]
SD = SD.loc[SD.index.dropna()]
SPI = SPI.loc[SPI.index.dropna()]
TD = TD.loc[TD.index.dropna()]
WD = WD.loc[WD.index.dropna()]

# figure
fig, ax = plt.subplots(1,1, sharex=True, figsize=(8, 6.2), constrained_layout=True)
i=0
dfs = [DA, EDC, ODC, LDC, SD, DF, EDML, SP, SPI, WD]
labels = ['Dome A', 'EPICA Dome C', 'Old Dome C', 'Little Dome C', 
          'Siple Pole', 'Dome Fuji', 'EDML', 
          'PS1', 'SPICE', 'WAIS Divide']
cmap = cmaps.tableau_10  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
ax.set_prop_cycle(color=colors)
ax.plot(vostok, label='Vostok', c='k')
for df in dfs:
    ax.plot(df, label=labels[i])
    i=i+1
ax.plot(TD, label='Taylor Dome', marker='s', linestyle='None', c='grey')
    

#
ax.set_xlim(-50, 7250)
ax.set_ylim(0, 1.6)
ax.set_ylabel('$^{10}$Be concentration (10$^5$ at/g)', fontsize=16)
ax.set_xlabel('Age (yr BP)', fontsize=16)

# Colors of scatter plots based on a colormap
#colormap = cm.Set1
#for i in [0,1]:
#    colorst = [colormap(i) for i in np.linspace(0, 1, 12]
#    for t,j1 in enumerate(ax.collections):
#        j1.set_color(colorst[t])
        
ax.legend(ncol=3, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='upper right', borderaxespad=0.3)

# show
plt.show()

# save
fig.savefig(cwd+'/fig04_all_10Be_conc_data_time_series.pdf', dpi=300)

