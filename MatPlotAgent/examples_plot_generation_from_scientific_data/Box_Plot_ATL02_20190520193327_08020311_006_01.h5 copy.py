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


    # box plot
    plt.boxplot(elev)
    plt.ylabel(longname)
    plt.title(longname+' Distribution')
    plt.show()




