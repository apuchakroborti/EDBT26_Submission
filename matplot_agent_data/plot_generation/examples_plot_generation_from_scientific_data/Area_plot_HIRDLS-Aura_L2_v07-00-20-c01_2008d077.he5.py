import matplotlib.pyplot as plt
import numpy as np

import h5py

# FILE_NAME = 'HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5'
FILE_NAME = '/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/GES_DISC/HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5'

with h5py.File(FILE_NAME, mode='r') as f:

    dset_var = f['/HDFEOS/SWATHS/HIRDLS/Data Fields/O3']
    dset_pres = f['/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Pressure']
    dset_time = f['/HDFEOS/SWATHS/HIRDLS/Geolocation Fields/Time']

    # Read the data.
    data = dset_var[0,:]
    pressure = dset_pres[:]
    # time = dset_time[0]
    time = dset_time[0:121]

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


    # Area Plot  
    plt.fill_between(time, pressure, color="skyblue", alpha=0.4)
    plt.plot(time, pressure, color="Slateblue", alpha=0.6)
    plt.xlabel(time_title)
    plt.ylabel(pres_title)
    plt.title(pres_title+' Over '+time_title)
    plt.show()


