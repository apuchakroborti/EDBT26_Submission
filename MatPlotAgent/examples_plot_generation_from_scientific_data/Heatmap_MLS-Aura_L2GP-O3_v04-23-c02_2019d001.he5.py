import h5py
import seaborn as sns

import numpy as np
import matplotlib.pyplot as plt


# FILE_NAME = "MLS-Aura_L2GP-O3_v04-23-c02_2019d001.he5"
FILE_NAME = '/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/GES_DISC/MLS-Aura_L2GP-O3_v04-23-c02_2019d001.he5'
with h5py.File(FILE_NAME, mode='r') as f:
    dset_var = f['HDFEOS/SWATHS/O3/Data Fields/L2gpValue']
    dset_lev = f['HDFEOS/SWATHS/O3/Geolocation Fields/Pressure']
    time = f['HDFEOS/SWATHS/O3/Geolocation Fields/Time']
    time_70 = f['HDFEOS/SWATHS/O3/Geolocation Fields/Time'][:70]

    # Read the data.
    # The latitude is not monotonic. Subset points that are monotonic.
    data = dset_var[:70,:]


    # Read the needed attributes.
    # String attributes actually come in as the bytes type and should
    # be decoded to UTF-8 (python3).
    data_units = dset_var.attrs['Units'].decode()
    lev_units = dset_lev.attrs['Units'].decode()

    data_title = dset_var.attrs['Title'].decode()
    lev_title = dset_lev.attrs['Title'].decode()

    # Handle fill value.
    fillvalue = dset_var.attrs['_FillValue']
    data[data == fillvalue] = np.nan
    data = np.ma.masked_array(data, np.isnan(data))

    
    time = time_70
    pressure = dset_lev
    data = data

    # take only 5 points to show properly
    data = dset_var[:5,:5]
    pressure = pressure[:5]
    time = time[:5]
    print('Shape of data: ', data.shape)
    print('Shape of pressure: ', pressure.shape)
    print('Shape of time: ', time.shape) 

    # Create a heatmap
    plt.figure(figsize=(14, 6))
    sns.heatmap(data, annot=True, cmap='viridis', xticklabels=time, yticklabels=pressure)

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Heatmap of Time vs Pressure')

    # Show the plot
    plt.show()
