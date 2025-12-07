"""
Copyright (C) 2014 John Evans

This example code illustrates how to access and visualize a GES DISC HIRDLS
HDF-EOS5 swath file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python HIRDLS-Aura_L2_v07-00-20-c01_2008d077.he5.py

The HDF-EOS5 file must be in your current working directory.

Tested under: Python 3.7.3 :: Anaconda
Last updated: 2019-11-04
"""

import datetime
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

import h5py
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter

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

    # The date is stored as a six-digit number, YYYYMM.  Convert it into
    # a string.
    # datestr = datetime.datetime(1993,1,1) + datetime.timedelta(seconds=time)


    # working
    """
    
    7. Area Plot
Use Case: To visualize cumulative soil moisture over time.
Graph Description: Similar to a line plot but filled under the line, showing the "area" covered by soil moisture over time.
Benefit: Highlights changes in cumulative values.
    """
  
    plt.fill_between(time, pressure, color="skyblue", alpha=0.4)
    plt.plot(time, pressure, color="Slateblue", alpha=0.6)
    plt.xlabel(time_title)
    plt.ylabel(pres_title)
    plt.title(pres_title+' Over '+time_title)
    plt.show()



    
    # not working due to shape mismatch
    """
    6. Scatter Plot
    Use Case: To explore relationships between soil moisture and another variable, like temperature or rainfall.
    Graph Description: A scatter plot with soil moisture on one axis and another variable (e.g., temperature) on the other.
    Benefit: This can help to see how soil moisture is affected by environmental factors.
    """


    # temperature = [20, 21, 19, 23, 24, 18, 22, 21, 20]
    # moisture = [0.3, 0.32, 0.28, 0.35, 0.37, 0.25, 0.34, 0.33, 0.3]
    print('Shape of dset_pres/pressure: ', pressure.shape)
    print('Shape of dset_time/time: ', dset_time.shape)
    print('Shape of dset_time/time: ', dset_time[0].shape)
    

    
    plt.scatter(time, pressure)
    plt.xlabel(time_title)
    plt.ylabel(pres_title)
    plt.title(pres_title+' vs '+time_title)
    plt.show()
    

  
  
    # not relevant to this data
    """
    5. Bar Plot
    Use Case: To visualize soil moisture levels across different categories (e.g., different locations or sensors).
    Graph Description: A bar plot where each bar represents soil moisture for different time points or categories.
    Benefit: This can show comparisons of soil moisture across different conditions.
    """
    categories = ['Location 1', 'Location 2', 'Location 3']
    moisture_levels = [0.23, 0.45, 0.35]

    plt.bar(categories, moisture_levels)
    plt.ylabel('Soil Moisture')
    plt.title('Soil Moisture by Location')
    plt.show()

    """
    plt.plot(data, pressure)

    # Save some screen space by using scientific notation for the xtick labels.
    formatter = plt.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.xlabel('{0} ({1})'.format(data_title, data_units))
    plt.ylabel('{0} ({1})'.format(pres_title, pres_units))

    basename = os.path.basename(FILE_NAME)
    plt.title('{0}\n{1} at {2}'.format(basename, data_title,
        datestr.strftime('%Y-%m-%d %H:%M:%S')))

    # This is useful for putting high pressure at the bottom.
    plt.gca().invert_yaxis()

    # Use log scale.
    plt.gca().set_yscale('log')

    # %g will take a number that could be represented as %f (a simple float or
    # double) or %e (scientific notation) and return it as the shorter of the
    # two.
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
    
    fig = plt.gcf()
    
    pngfile = "{0}.py.png".format(basename)    
    fig.savefig(pngfile)
    """



