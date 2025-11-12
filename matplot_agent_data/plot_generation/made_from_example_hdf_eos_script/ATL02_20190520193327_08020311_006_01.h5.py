"""

This example code illustrates how to access and visualize a ICESat-2 ATL02
file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage: save this script and run

    $python ATL02_20190520193327_08020311_006_01.h5.py

The HDF5 file must be in your current working directory.

Tested under: Python 3.9.13 :: Miniconda (64-bit)
Last Update: 2024-02-26
"""

import datetime
import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import h5py
import numpy as np

# FILE_NAME = "ATL02_20190520193327_08020311_006_01.h5"
FILE_NAME ='/Users/apukumarchakroborti/gsu_research/llam_test/ACL_DIRS/ICESat_2/ATL02_20190520193327_08020311_006_01.h5'
with h5py.File(FILE_NAME, mode="r") as f:

    latvar = f["/gpsr/navigation/latitude"]
    latitude = latvar[:]

    lonvar = f["/gpsr/navigation/longitude"]
    longitude = lonvar[:]

    dsetname = "/atlas/pce1/background/bg_cnt_50shot_s"
    elevvar = f[dsetname]
    print('bg_cnt_50shot_s Shape: ', elevvar.shape)

    elev = elevvar[:]
    units = elevvar.attrs["units"]
    units = units.decode("ascii", "replace")
    longname = elevvar.attrs["long_name"]
    longname = longname.decode("ascii", "replace")

    timevar = f["/atlas/pce1/background/delta_time"]
    time = timevar[:]
    print('delta_time Shape: ', time.shape)

    """
    1. Line Plot (Time Series)
Use Case: To visualize soil moisture over time.
Graph Description: A line plot where the x-axis represents time and the y-axis represents soil moisture values.
Benefit: This shows how soil moisture fluctuates over a period, revealing patterns like dry or wet seasons.
    """
    # Line plot example
    plt.plot(time, elev)
    plt.xlabel('Time')
    plt.ylabel(longname)
    plt.title(longname+' over Time')
    plt.show()


    """
    2. Histogram
Use Case: To analyze the distribution of soil moisture values.
Graph Description: A histogram where the x-axis represents the range of soil moisture values, and the y-axis represents frequency.
Benefit: This shows how often certain soil moisture levels occur, helping to identify if the data is skewed toward dry or wet conditions.
    """
    # histogram
    plt.hist(elev, bins=20, edgecolor='black')
    plt.xlabel(longname)
    plt.ylabel('Frequency')
    plt.title('Distribution of '+longname)
    plt.show()



    """
    3. Box Plot
Use Case: To summarize the distribution of soil moisture.
Graph Description: A box plot showing the minimum, first quartile, median, third quartile, and maximum soil moisture values.
Benefit: It provides a summary of the data's central tendency, variability, and potential outliers.
    """

    # box plot
    plt.boxplot(elev)
    plt.ylabel(longname)
    plt.title(longname+' Distribution')
    plt.show()



    """
    4. Cumulative Distribution Function (CDF)
Use Case: To analyze the cumulative probability distribution of soil moisture.
Graph Description: A line plot showing the cumulative distribution of soil moisture values.
Benefit: This can show the probability of moisture values being below a certain threshold
    
    """ 
    sorted_data = np.sort(elev)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data)-1)

    plt.plot(sorted_data, yvals)
    plt.xlabel(longname)
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution of '+longname)
    plt.show()

    

    
    """
    soil_moisture = elevvar[:]
    plt.hist(soil_moisture, bins=20, edgecolor='black')
    plt.xlabel('Soil Moisture')
    plt.ylabel('Frequency')
    plt.title('Distribution of Soil Moisture')
    plt.show()

    """
    """
    # Make a split window plot.  First plot is time vs. counts.
    fig = plt.figure(figsize=(10, 10))
    ax1 = plt.subplot(2, 1, 1)
    elapsed_time = time - time[0]
    timebase = datetime.datetime(2018, 1, 1, 0, 0, 0) + datetime.timedelta(
        seconds=time[0]
    )
    timedatum = timebase.strftime("%Y-%m-%dT%H:%M:%SZ")
    tunits = "Seconds from " + timedatum

    ax1.plot(elapsed_time, elev, "bo")
    ax1.set_xlabel(tunits)
    ax1.set_ylabel(str(units))

    basename = os.path.basename(FILE_NAME)

    ax1.set_title("{0}\n{1}\n{2}".format(basename, dsetname, longname))
    # Find the middle location.
    lat_m = latitude[int(latitude.shape[0] / 2)]
    lon_m = longitude[int(longitude.shape[0] / 2)]
    orth = ccrs.Orthographic(
        central_longitude=lon_m, central_latitude=lat_m, globe=None
    )

    # The 2nd plot is the trajectory.
    ax3 = plt.subplot(2, 1, 2, projection=orth)

    # Put grids.
    gl = ax3.gridlines(draw_labels=True, dms=True)

    ax3.set_global()
    # Put coast lines.
    ax3.coastlines()
    ax3.plot(
        longitude,
        latitude,
        color="blue",
        linewidth="2",
        transform=ccrs.Geodetic(),
    )

    # Annotate the starting point.  Offset the annotation text by 200 km.
    ax3.plot(
        longitude[0],
        latitude[0],
        marker="o",
        color="red",
        transform=ccrs.Geodetic(),
    )
    ax3.text(
        longitude[0] + 1.0,
        latitude[0],
        "START",
        color="red",
        transform=ccrs.Geodetic(),
    )
    ax3.set_title("Trajectory of Flight Path")

    # Add spacing between subplots.
    fig.tight_layout(pad=3.0)

    fig = plt.gcf()
    pngfile = "{0}.py.png".format(basename)
    fig.savefig(pngfile)
    """
