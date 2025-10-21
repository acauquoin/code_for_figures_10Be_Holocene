#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#==============================================================================
# Import the packages
#==============================================================================

from netCDF4 import Dataset as NetCDFFile
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib.path as mpath
import matplotlib.patheffects as path_effects
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import cartopy.feature as feature
import os

# get current directory
cwd = os.getcwd()

# elevation file
ifile_elev = cwd + '/elev_nb_lat_lon.nc'
ds_elev = xr.open_dataset(ifile_elev)
elev = ds_elev.elev

# location of 10Be data
ifile_stations = cwd + '/location_stations.csv'
ifile_horiuchi59 = cwd + '/horiuchi_NIMPRB_2022_JAREs59.csv'
ifile_horiuchi60 = cwd + '/horiuchi_NIMPRB_2022_JAREs60.csv'
ifile_berggren = cwd + '/berggren_NIMPRB_2013_table2.csv'
#
station = np.genfromtxt(ifile_stations, unpack=True, delimiter=";", usecols = (0), dtype=str)
lat_station, lon_station = np.genfromtxt(ifile_stations, unpack=True, delimiter=";", usecols = (1,2))
lat_horiuchi59, lon_horiuchi59 = np.genfromtxt(ifile_horiuchi59, skip_header=1, unpack=True, delimiter=";", usecols = (1,2))
lat_horiuchi60, lon_horiuchi60 = np.genfromtxt(ifile_horiuchi60, skip_header=1, unpack=True, delimiter=";", usecols = (1,2))
lat_berggren, lon_berggren = np.genfromtxt(ifile_berggren, skip_header=1, unpack=True, delimiter=";", usecols = (0,1))
#
for i in range(len(station)):
    if (station[i] == "South Pole") or (station[i] == "Taylor Dome") or (station[i] == "Law Dome") or (station[i] == "Siple Dome") or (station[i] == "WAIS Divide") or (station[i] == "Berkner Island"):
        station[i] = station[i].replace(" ", "\n")

# Compute a circle in axes coordinates, which we can use as a boundary
# for the map. We can pan/zoom as much as we like - the boundary will be
# permanently circular.
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)

# palette pour colorbar
levels_ps = np.arange(200,3801,200)
n_colors_ps = len(levels_ps) + 1
cmap = plt.get_cmap('RdYlBu_r', n_colors_ps)
colors_ps = cmap(range(cmap.N))
cmap, norm = mc.from_levels_and_colors(levels_ps, colors_ps, extend='both')

fig, ax = plt.subplots(1, 1, figsize=(5.5, 6.3), subplot_kw=dict(projection=ccrs.SouthPolarStereo()), constrained_layout=True)
plt.rcParams.update({'font.family': 'sans-serif', 'text.usetex': False})
#
ax.set_extent([-180, 180, -90, -65.5], crs=ccrs.PlateCarree())
ax.coastlines(zorder=101, linewidth=1.5)
#ax.set_boundary(circle, transform=ax.transAxes)
cs_reg = ds_elev.elev.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), x='lon', y='lat', norm=norm, cmap=cmap, edgecolors='face', shading='nearest', extend='both', add_colorbar=False)
ax.scatter(lon_station, lat_station, c='k', s=80, marker='o', edgecolors='white', linewidth=1, zorder=104, transform=ccrs.PlateCarree())
l1 = ax.scatter(lon_horiuchi59, lat_horiuchi59, facecolors="None", edgecolors='k', s=80, marker='^', linewidth=1, zorder=103, transform=ccrs.PlateCarree())
ax.scatter(lon_horiuchi60, lat_horiuchi60, facecolors="None", edgecolors='k', s=80, marker='^', linewidth=1, zorder=103, transform=ccrs.PlateCarree())
l2 = ax.scatter(lon_berggren, lat_berggren, facecolors="None", edgecolors='k', s=80, marker='s', linewidth=1, zorder=103, transform=ccrs.PlateCarree())
#
for label, lon_scatter, lat_scatter in zip(station, lon_station, lat_station):
    at_x, at_y = ax.projection.transform_point(lon_scatter, lat_scatter, src_crs=ccrs.PlateCarree())
    if (label == "South\nPole") or (label == "Taylor\nDome") or (label == "Law\nDome") or (label == "Siple\nDome"):
        text = ax.annotate(label, xy=(at_x, at_y), xytext=(at_x+70000,at_y), fontsize=12, fontweight='bold', va='center', ha='left', zorder=301)
    elif (label == "Talos Dome") or (label == "Dome F"):
        text = ax.annotate(label, xy=(at_x, at_y), xytext=(at_x+70000,at_y), fontsize=12, fontweight='bold', va='top', ha='left', zorder=301)
#    elif (label == "Kohnen"):
#        text = ax.annotate(label, xy=(at_x, at_y), xytext=(at_x+70000,at_y-70000), fontsize=12, fontweight='bold', va='top', ha='left', zorder=301)
    else:
        text = ax.annotate(label, xy=(at_x, at_y), xytext=(at_x,at_y+40000), fontsize=12, fontweight='bold', va='bottom', ha='left', zorder=301)
    text.set_path_effects([path_effects.Stroke(foreground='white', linewidth=2), path_effects.Normal()])
[x.set_linewidth(0) for x in ax.spines.values()]
#
# Colorbar
cbar=plt.colorbar(cs_reg, orientation="horizontal", ax=ax, pad=0.015, extend='both', ticks=levels_ps[::2], aspect=40)
cbar.ax.tick_params(labelsize=12)
cbar.set_label('Elevation (m)', size=14, labelpad=7)

# legend
ax.legend([l1, l2], ['JARE59/60', 'JASE'], ncol=1, handletextpad=0.5, fontsize=12, columnspacing=1.75, loc='upper right', borderaxespad=0.3, frameon=False)

# Show
plt.show()

# save figure
fig.savefig(cwd+'/fig01_antarctic_map_10Be_stations.pdf', dpi=300)
