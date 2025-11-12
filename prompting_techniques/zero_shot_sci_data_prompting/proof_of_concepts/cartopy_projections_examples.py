"""Cartopy is a Python library designed for geospatial data visualization. It replaces **Basemap** as the preferred library for handling maps and projections in Python. Cartopy provides a wide range of map projections, integrations with data sources, and a simple API for creating high-quality visualizations. Below, I'll walk you through some common use cases of Cartopy with code examples for each scenario.

### Installation
First, ensure you have Cartopy installed:
```bash
pip install cartopy
```

### 1. **Basic Map Plotting**

You can create a simple map using Cartopy by choosing a projection and plotting coastlines, borders, or any geographic features.

```python

"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Create a basic map with PlateCarree projection
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

plt.show()

"""
```

### 2. **Changing Projections**

Cartopy supports a variety of projections. Below is an example of a **Robinson projection**.

```python
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Robinson())

ax.coastlines()
plt.title("Robinson Projection")

plt.show()

"""```

### 3. **Adding Gridlines and Labels**

You can customize maps by adding gridlines and labeling latitudes and longitudes.

```python
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.coastlines()
ax.gridlines(draw_labels=True)  # Draw gridlines with labels

plt.show()

"""```

### 4. **Adding Features: Rivers, Borders, Lakes**

Cartopy includes a set of predefined features that you can overlay onto your map, such as rivers, borders, and lakes.

```python
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add features like coastlines, rivers, and borders
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':', color='black')
ax.add_feature(cfeature.RIVERS, color='blue')

plt.show()

"""```

### 5. **Plotting Points (Latitude/Longitude)**

You can also plot specific points on the map by providing their latitudes and longitudes.

```python
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.coastlines()

# Coordinates for cities
cities = {'London': (-0.1276, 51.5074), 'Paris': (2.3522, 48.8566), 'New York': (-74.0060, 40.7128)}
for city, (lon, lat) in cities.items():
    ax.plot(lon, lat, marker='o', color='red', markersize=6, transform=ccrs.Geodetic())
    ax.text(lon + 3, lat - 3, city, transform=ccrs.Geodetic())

plt.show()

"""```

### 6. **Working with Satellite Data (Geospatial Data)**

You can load geospatial datasets, such as NetCDF, and plot the data on a map. Cartopy integrates well with tools like **xarray** for handling data.

```python
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr

# Load a NetCDF dataset using xarray
ds = xr.open_dataset('path/to/satellite_data.nc')

# Extract a data variable (e.g., temperature)
data = ds['temperature'].isel(time=0)  # Selecting first time slice

# Create a map and plot data on it
fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

# Plot temperature data
data.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm', cbar_kwargs={'label': 'Temperature (K)'})

plt.show()

"""```

### 7. **Shapefile Integration**

You can overlay shapefiles on your Cartopy maps to show regions, countries, or any other geographic boundaries.

```python
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

# Path to the shapefile
shapefile = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_0_countries')

# Read shapefile and plot
reader = shpreader.Reader(shapefile)
countries = reader.records()

for country in countries:
    ax.add_geometries([country.geometry], ccrs.PlateCarree(), edgecolor='black')

plt.show()

"""```

### 8. **Projection Examples: Lambert Conformal, Mollweide, Mercator**

#### Lambert Conformal Conic
```python
"""
fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.LambertConformal())
ax.coastlines()
plt.show()

"""```

#### Mollweide Projection
```python

"""
fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.Mollweide())
ax.coastlines()
plt.show()

"""```

#### Mercator Projection
```python
"""

fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines()
plt.show()

"""```

### 9. **Vector Data (Wind, Ocean Currents)**

You can visualize vector data like wind or ocean currents using quiver plots.

```python
"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

# Generate some fake data
lon, lat = np.meshgrid(np.linspace(-180, 180, 30), np.linspace(-90, 90, 15))
u = np.sin(np.radians(lat))  # Wind in the u-direction
v = np.cos(np.radians(lon))  # Wind in the v-direction

# Plot wind vectors
ax.quiver(lon, lat, u, v, transform=ccrs.PlateCarree())

plt.show()


"""```

### 10. **Time Series on Maps**

You can plot time series data on maps to show changes over time, such as sea surface temperatures, atmospheric pressure, or population growth.

```python
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

# Sample data
times = np.linspace(0, 2 * np.pi, 10)
sea_surface_temp = np.sin(times)

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
ax.coastlines()

for t, temp in zip(times, sea_surface_temp):
    ax.scatter(t * 30, temp * 10, color='blue', transform=ccrs.PlateCarree())  # Plot at different longitudes over time

plt.show()

"""```

### 11. **Interactive Map with Matplotlib Widgets**

You can create interactive maps using Matplotlib widgets or integrate Cartopy with Jupyter notebooks for interactive maps.

---

### Summary of Use Cases:
1. **Basic Maps**: Plotting coastlines, borders, and grids.
2. **Projections**: Choosing appropriate projections for different regions.
3. **Features**: Overlaying features like rivers, borders, lakes.
4. **Geospatial Data**: Handling NetCDF and satellite data.
5. **Shapefiles**: Using shapefiles for administrative or custom boundaries.
6. **Vector Fields**: Plotting wind, ocean currents, and vector fields.
7. **Time Series**: Plotting dynamic data over time on a geographic scale.

Cartopy's versatility makes it suitable for a wide variety of geospatial applications, from basic geographic visualizations to complex analyses of climate or environmental data.
"""