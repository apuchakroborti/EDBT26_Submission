import matplotlib.pyplot as plt
import numpy as np

import h5py

import seaborn as sns


# FILE_NAME = 'HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5'
FILE_NAME = '/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/GES_DISC/HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5'

with h5py.File(FILE_NAME, mode='r') as f:

    dset_var = f['/HDFEOS/SWATHS/HIRDLS/Data Fields/O3']
    dset_pres = f['/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Pressure']
    dset_time = f['/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Time']

    # Read the data.
    data = dset_var[0,:]
    print('Shape of data: ', data.shape)

    pressure = dset_pres[:]
    print('Shape of pressure: ', pressure.shape)

    # time = dset_time[0]
    time = dset_time[0:121]
    print('Shape of time: ', time.shape)

    # Read the needed attributes.
    # String attributes actually come in as the bytes type and should
    # be decoded to UTF-8 (python3).
    data_units = dset_var.attrs['Units'].decode()
    pres_units = dset_pres.attrs['Units'].decode()
    data_title = dset_var.attrs['Title'].decode()
    time_title = dset_time.attrs['Title'].decode()
    pres_title = dset_pres.attrs['Title'].decode()

    fillvalue = dset_var.attrs['_FillValue']
    data[data == fillvalue] = np.nan


    # Heatmap


    # Replace these with your actual time and pressure data
    # time = np.linspace(0, 100, 12)  # Example time data (12 values)
    # pressure = np.linspace(0, 50, 10)  # Example pressure data (10 values)
    # data = np.random.rand(10, 12)  # Replace with actual data matching the shape of time and pressure

    # Create a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(data, annot=True, cmap='viridis', xticklabels=time, yticklabels=pressure)

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Heatmap of Time vs Pressure')

    # Show the plot
    plt.show()  
    


