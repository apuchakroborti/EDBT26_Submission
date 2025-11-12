import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Constants
FILE_NAME = '/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/ICESat_2/ATL11_051911_0321_006_06.h5'
FILL_VALUE = -9999  # Assuming _FillValue is a special value for missing data

# Open the HDF5 file
file = h5py.File(FILE_NAME, 'r')

# Read datasets
longitude = file['pt1/longitude'][:]
latitude = file['pt1/latitude'][:]
h_corr = file['pt1/h_corr'][:]
print(h_corr)

# Extract metadata from /pt1/h_corr dataset
units = file['pt1/h_corr'].attrs['units']
long_name = file['pt1/h_corr'].attrs['long_name']
fill_value = file['pt1/h_corr'].attrs['_FillValue']

# Replace fill value with NaN
h_corr[h_corr == fill_value] = np.nan
masked_data = np.ma.masked_where(np.isnan(h_corr), h_corr)

# Create a map projection
plt.figure(figsize=(10, 8))
m = Basemap(projection='merc', llcrnrlon=-180, urcrnrlon=180, llcrnrlat=-80, urcrnrlat=80)
m.drawcoastlines()
m.drawparallels(np.arange(-90, 90, 30), labels=[True, False, False, True])
m.drawmeridians(np.arange(0, 360, 60), labels=[True, False, False, True])
m.scatter(longitude, latitude, latlon=True, c=masked_data, cmap='viridis')

# Add colorbar and title
cbar = m.colorbar()
cbar.set_label(units)
plt.title(f'{os.path.basename(FILE_NAME)} - {long_name}')

# Save the plot to a PNG file
output_file = os.path.splitext(FILE_NAME)[0] + '.png'
plt.savefig(output_file, format='png')

# Close the HDF5 file and Matplotlib figure
file.close()
plt.close()