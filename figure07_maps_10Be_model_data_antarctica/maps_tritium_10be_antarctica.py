#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#==============================================================================
# Import the packages
#==============================================================================

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib.path as mpath
import matplotlib.patheffects as path_effects
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import cartopy.feature as feature
import os
from cdo import *

cdo = Cdo()

# get current directory
cwd = os.getcwd()

# Model Files
ifile_totdep_10be = cwd+'/tot_be10_antarctica.nc'
ifile_totdep_10be_conc = cwd+'/tot_be10_conc_antarctica.nc'
ifile_precip = cwd+'/aprt_antarctica.nc'
ifile_jan_surf = cwd+'/T63GR15_jan_surf.nc'
ifile_flux_div_accu = cwd+'/tot_be10_div_precip_antarctica.nc'

# Read NetCDF
ds_totdep_10be      = xr.open_dataset(ifile_totdep_10be)
ds_totdep_10be_conc = xr.open_dataset(ifile_totdep_10be_conc)
ds_precip           = xr.open_dataset(ifile_precip)
ds_flux_div_accu    = xr.open_dataset(ifile_flux_div_accu)

# fldmean
ifile_totdep_10be_mean      = cdo.fldmean(input='-selvar,tot_be10 '+ifile_totdep_10be, options='--reduce_dim -f nc -r')
ifile_totdep_10be_conc_mean = cdo.fldmean(input='-selvar,tot_be10_conc '+ifile_totdep_10be_conc, options='--reduce_dim -f nc -r')

# extract variables
totdep_10be          = ds_totdep_10be.tot_be10.squeeze(drop=True)
totdep_10be_conc     = ds_totdep_10be_conc.tot_be10_conc.squeeze(drop=True)
totdep_10be_div_accu = ds_flux_div_accu.tot_be10.squeeze(drop=True)
totdep_10be_div_accu = totdep_10be_div_accu / 100000.

# calculate field mean values
ds_totdep_10be_mean      = xr.open_dataset(ifile_totdep_10be_mean)
ds_totdep_10be_conc_mean = xr.open_dataset(ifile_totdep_10be_conc_mean)
totdep_10be_mean      = ds_totdep_10be_mean.tot_be10
totdep_10be_conc_mean = ds_totdep_10be_conc_mean.tot_be10_conc

# relative values (division by the mean)
totdep_10be_rel       = totdep_10be / totdep_10be_mean
totdep_10be_conc_rel = totdep_10be_conc / totdep_10be_conc_mean

# Import 10Be data locations
ifile_data_loc = cwd+'/site_locations.csv'
station = np.genfromtxt(ifile_data_loc, unpack=True, skip_header=1, delimiter=";", usecols = (0), dtype='str')
lat_data, lon_data = np.genfromtxt(ifile_data_loc, unpack=True, skip_header=1, delimiter=";", usecols = (1, 2))

# get 10Be modeled values at stations locations
print ('10Be modeled values at stations locations')
print ('station, 10Be_conc (1e5 at/g), 10Be_flux (at/m2/s), accu (g/cm2/yr), elevation (m)')
for i in range(len(lat_data)):
    beryllium_flux_modeled_value = cdo.remapnn("lon="+str(lon_data[i])+"_lat="+str(lat_data[i]), input='-selvar,tot_be10 '+ifile_totdep_10be, options='--reduce_dim -f nc', returnArray='tot_be10')
    beryllium_conc_modeled_value = cdo.remapnn("lon="+str(lon_data[i])+"_lat="+str(lat_data[i]), input='-selvar,tot_be10_conc '+ifile_totdep_10be_conc, options='--reduce_dim -f nc', returnArray='tot_be10_conc')
    accu_modeled_value = cdo.remapnn("lon="+str(lon_data[i])+"_lat="+str(lat_data[i]), input='-selvar,aprt '+ifile_precip, options='--reduce_dim -f nc', returnArray='aprt')
    accu_modeled_value = accu_modeled_value * 1000 / 10000 * (60*60*24*365)
    elev = cdo.remapnn("lon="+str(lon_data[i])+"_lat="+str(lat_data[i]), input='-selvar,OROMEA '+ifile_jan_surf, options='--reduce_dim -f nc', returnArray='OROMEA')
    print (station[i], beryllium_conc_modeled_value, beryllium_flux_modeled_value, accu_modeled_value, elev)

# Import 10Be data
ifile_data = cwd+'/mean_10Be_data_holocene.csv'
#station_map = np.genfromtxt(ifile_data, unpack=True, skip_header=1, delimiter=";", usecols = (0), dtype='str')
station_map = ["Siple\nDome", "WAIS\nDivide", "PS1", 'EDML', 'EDC', 'LDC', 'ODC', 'Vostok', 'Dome F', 'Dome A', 'SPICE']
va_station_map = ["top", "bottom", "top", "bottom", "bottom", "bottom", "top", "bottom", "bottom", "bottom", "bottom"]
ha_station_map = ["left", "left", "left", "left", "right", "left", "left", "left", "left", "left", "center"]
lon_offset = [-2, 0, 70, 0, 2, 0, 0, 0, 0, 0, 50]
lat_offset = [0, -0.2, 0.3, 0, 0, 0.5, 0, 0, 0, 0, 1]
lat_data, lon_data, conc_data, accu_data, flux_data = np.genfromtxt(ifile_data, unpack=True, skip_header=1, delimiter=";", usecols = (1, 2, 3, 4, 5))
#
flux_data_rel = flux_data / np.nanmean(flux_data)
flux_data_div = flux_data / (accu_data * 10000 / (60*60*24*365)) / 100000.
idx = np.isfinite(flux_data)

# circle in axes coordinates
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)

# # figure
# fig, ax = plt.subplots(1, 2, figsize=(11.02,  6.35), subplot_kw=dict(projection=ccrs.SouthPolarStereo()), constrained_layout=True, frameon=False)
# plt.rcParams.update({'font.family': 'sans-serif', 'text.usetex': False})
# #
# levels_ps = np.arange(0.1,1.01,0.05)
# n_colors_ps = len(levels_ps) + 1
# cmap = plt.get_cmap('RdYlBu_r', n_colors_ps)
# colors_ps = cmap(range(cmap.N))
# cmap, norm = mc.from_levels_and_colors(levels_ps, colors_ps, extend='both')
# #
# cs = totdep_10be_div_accu.plot.pcolormesh(cmap=cmap, norm=norm, ax=ax[0], transform=ccrs.PlateCarree(), x='lon', y='lat', edgecolors='face', shading='nearest', extend='both', add_colorbar=False)
# ax[0].scatter(lon_data[idx], lat_data[idx], c=flux_data_div[idx], s=100, cmap=cmap, marker='o', edgecolors='k', linewidth=1, norm=norm, zorder=103, transform=ccrs.PlateCarree())
# for i, label in enumerate(station_map):
#     txt = ax[0].annotate(label, (lon_data[i]+lon_offset[i], lat_data[i]+lat_offset[i]), fontsize=14, color='k', fontweight='bold', horizontalalignment=ha_station_map[i], verticalalignment=va_station_map[i], transform=ccrs.PlateCarree(), zorder=600)
#     txt.set_path_effects([path_effects.Stroke(foreground='white', linewidth=2), path_effects.Normal()])
# ax[0].set_extent([-180, 180, -90, -65.5], crs=ccrs.PlateCarree())
# ax[0].coastlines(zorder=101)
# ax[0].text(0.005, 0.995, '(a)', fontsize=18, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=ax[0].transAxes)
# [x.set_linewidth(0) for x in ax[0].spines.values()]
# #
# cbar=plt.colorbar(cs, orientation="horizontal", ax=ax[0], pad=0.015, extend='both', ticks=levels_ps[::2], aspect=40)
# cbar.ax.tick_params(labelsize=14)
# cbar.set_label('$\mathsf{^{10}}$Be flux / precipitation (10$^5$ at.g$^{-1}$)', size=14, labelpad=7)
# #
# #
# levels_ps = np.arange(0.1,1.91,0.1)
# n_colors_ps = len(levels_ps) + 1
# cmap = plt.get_cmap('RdYlBu_r', n_colors_ps)
# colors_ps = cmap(range(cmap.N))
# cmap, norm = mc.from_levels_and_colors(levels_ps, colors_ps, extend='both')
# #
# cs = totdep_10be_rel.plot.pcolormesh(cmap=cmap, norm=norm, ax=ax[1], transform=ccrs.PlateCarree(), x='lon', y='lat', edgecolors='face', shading='nearest', extend='both', add_colorbar=False)
# ax[1].scatter(lon_data[idx], lat_data[idx], c=flux_data_rel[idx], s=100, cmap=cmap, marker='o', edgecolors='k', linewidth=1, norm=norm, zorder=103, transform=ccrs.PlateCarree())
# for i, label in enumerate(station_map):
#     txt = ax[1].annotate(label, (lon_data[i]+lon_offset[i], lat_data[i]+lat_offset[i]), fontsize=14, color='k', fontweight='bold', horizontalalignment=ha_station_map[i], verticalalignment=va_station_map[i], transform=ccrs.PlateCarree(), zorder=600)
#     txt.set_path_effects([path_effects.Stroke(foreground='white', linewidth=2), path_effects.Normal()])
# ax[1].set_extent([-180, 180, -90, -65.5], crs=ccrs.PlateCarree())
# ax[1].coastlines(zorder=101)
# ax[1].text(0.005, 0.995, '(b)', fontsize=18, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=ax[1].transAxes)
# [x.set_linewidth(0) for x in ax[1].spines.values()]
# #
# cbar=plt.colorbar(cs, orientation="horizontal", ax=ax[1], pad=0.015, extend='both', ticks=levels_ps[::2], aspect=40)
# cbar.ax.tick_params(labelsize=14)
# cbar.set_label('$\mathsf{^{10}Be\ flux}$ (rel)', size=14, labelpad=7)

# # show
# plt.show()

# # save
# #fig.savefig(cwd+'/fig06_maps_10Be_model_data_antarctica.pdf', dpi=300)


# figure
fig, ax = plt.subplots(1, 2, figsize=(11.02,  6.35), subplot_kw=dict(projection=ccrs.SouthPolarStereo()), constrained_layout=True, frameon=False)
plt.rcParams.update({'font.family': 'sans-serif', 'text.usetex': False})
#
levels_ps = np.arange(0.1,1.01,0.05)
n_colors_ps = len(levels_ps) + 1
cmap = plt.get_cmap('RdYlBu_r', n_colors_ps)
colors_ps = cmap(range(cmap.N))
cmap, norm = mc.from_levels_and_colors(levels_ps, colors_ps, extend='both')
#
cs = totdep_10be_conc.plot.pcolormesh(cmap=cmap, norm=norm, ax=ax[0], transform=ccrs.PlateCarree(), x='lon', y='lat', edgecolors='face', shading='nearest', extend='both', add_colorbar=False)
ax[0].scatter(lon_data[idx], lat_data[idx], c=conc_data[idx], s=100, cmap=cmap, marker='o', edgecolors='k', linewidth=1, norm=norm, zorder=103, transform=ccrs.PlateCarree())
for i, label in enumerate(station_map):
    txt = ax[0].annotate(label, (lon_data[i]+lon_offset[i], lat_data[i]+lat_offset[i]), fontsize=14, color='k', fontweight='bold', horizontalalignment=ha_station_map[i], verticalalignment=va_station_map[i], transform=ccrs.PlateCarree(), zorder=600)
    txt.set_path_effects([path_effects.Stroke(foreground='white', linewidth=2), path_effects.Normal()])
ax[0].set_extent([-180, 180, -90, -65.5], crs=ccrs.PlateCarree())
ax[0].coastlines(zorder=101)
ax[0].text(0.005, 0.995, '(a)', fontsize=18, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=ax[0].transAxes)
[x.set_linewidth(0) for x in ax[0].spines.values()]
#
cbar=plt.colorbar(cs, orientation="horizontal", ax=ax[0], pad=0.015, extend='both', ticks=levels_ps[::2], aspect=40)
cbar.ax.tick_params(labelsize=14)
cbar.set_label('$\mathsf{^{10}}$Be concentration (10$^5$ at.g$^{-1}$)', size=14, labelpad=7)
#
#
levels_ps = [30,  40, 50,  60,  70,  80,  90, 100, 110, 120, 130, 150, 170, 200, 230]
n_colors_ps = len(levels_ps) + 1
cmap = plt.get_cmap('RdYlBu_r', n_colors_ps)
colors_ps = cmap(range(cmap.N))
cmap, norm = mc.from_levels_and_colors(levels_ps, colors_ps, extend='both')
#
cs = totdep_10be.plot.pcolormesh(cmap=cmap, norm=norm, ax=ax[1], transform=ccrs.PlateCarree(), x='lon', y='lat', edgecolors='face', shading='nearest', extend='both', add_colorbar=False)
ax[1].scatter(lon_data[idx], lat_data[idx], c=flux_data[idx], s=100, cmap=cmap, marker='o', edgecolors='k', linewidth=1, norm=norm, zorder=103, transform=ccrs.PlateCarree())
for i, label in enumerate(station_map):
    txt = ax[1].annotate(label, (lon_data[i]+lon_offset[i], lat_data[i]+lat_offset[i]), fontsize=14, color='k', fontweight='bold', horizontalalignment=ha_station_map[i], verticalalignment=va_station_map[i], transform=ccrs.PlateCarree(), zorder=600)
    txt.set_path_effects([path_effects.Stroke(foreground='white', linewidth=2), path_effects.Normal()])
ax[1].set_extent([-180, 180, -90, -65.5], crs=ccrs.PlateCarree())
ax[1].coastlines(zorder=101)
ax[1].text(0.005, 0.995, '(b)', fontsize=18, fontweight='bold', horizontalalignment='left', verticalalignment='top', transform=ax[1].transAxes)
[x.set_linewidth(0) for x in ax[1].spines.values()]
#
cbar=plt.colorbar(cs, orientation="horizontal", ax=ax[1], pad=0.015, extend='both', ticks=levels_ps[::2], aspect=40)
cbar.ax.tick_params(labelsize=14)
cbar.set_label('$\mathsf{^{10}Be\ flux}$ (at.m$^{-2}$.s$^{-1}$)', size=14, labelpad=7)

# show
plt.show()

# save
fig.savefig(cwd+'/fig07_maps_10Be_model_data_antarctica_conc_and_flux.pdf', dpi=300)
