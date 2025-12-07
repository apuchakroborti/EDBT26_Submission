import matplotlib.pyplot as plt
import h5py
import numpy as np

# FILE_NAME = "ATL02_20190520193327_08020311_006_01.h5"
FILE_NAME ='/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/ICESat_2/ATL02_20190520193327_08020311_006_01.h5'
with h5py.File(FILE_NAME, mode="r") as f:

    dsetname = "/atlas/pce1/background/bg_cnt_50shot_s"
    elevvar = f[dsetname]
    print('bg_cnt_50shot_s Shape: ', elevvar.shape)

    elev = elevvar[:]
    units = elevvar.attrs["units"]
    units = units.decode("ascii", "replace")
    longname = elevvar.attrs["long_name"]
    longname = longname.decode("ascii", "replace")


   
    sorted_data = np.sort(elev)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data)-1)

    plt.plot(sorted_data, yvals)
    plt.xlabel(longname)
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of '+longname)
    plt.show()
