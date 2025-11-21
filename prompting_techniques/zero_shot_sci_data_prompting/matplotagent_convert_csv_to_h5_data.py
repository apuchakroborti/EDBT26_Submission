import os
import pandas as pd
import h5py


# input_file_directory= '/Users/apukumarchakroborti/gsu_research/MatPlotAgent-main/benchmark_data/data'
input_file_directory= '/home/achakroborti1/related_work/MatPlotAgent/benchmark_data/data'
# out_file_directory = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data'
out_file_directory = '/home/achakroborti1/llam_test/ai_lab2_llm_for_scientific_data/ai_lab2_llm_for_scientific_data/matplot_agent_data/plot_generation/csv_to_h5_data'
column_dictionary = {}

dtype_dic_76 = {'Womans millions of dollars': 'int32', 'Mens millions of dollars': 'int32'}
column_dictionary['76'] = dtype_dic_76

dtype_dic_77 = {'Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64',
             'Fish': 'float64', 'Cereals': 'float64', 'Starch': 'float64', 'Nuts': 'float64', 'Fruits and Vegetables': 'float64'}
column_dictionary['77'] = dtype_dic_77

dtype_dic_78 = {'0-60 mph(sec)': 'int32', 'Gas Mileage(mpg)': 'int32', 'Power(kW)': 'int32', 'Weight(kg)': 'int32', 'Engine Displacement(cc)': 'float64'}
column_dictionary['78'] = dtype_dic_78

dtype_dic_79 = {'Petal Length(cm)': 'float32', 'Petal Width(cm)': 'float32', 'Sepal Length(cm)': 'float32', 'Sepal Width(cm)': 'float32', 'Species': 'str'}
column_dictionary['79'] = dtype_dic_79
# no headers
# dtype_dic_80 = {'Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64',
            #  'Fish': 'float64', 'Cereals': 'float64', 'Starch': 'float64', 'Nuts': 'float64', 'Fruits & Vegetables': 'float64'}

# no meaning ful data only strings
# dtype_dic_81 = {'Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64',
#              'Fish': 'float64', 'Cereals': 'float64', 'Starch': 'float64', 'Nuts': 'float64', 'Fruits & Vegetables': 'float64'}

# json format data not needed right now
# dtype_dic_82 = {'Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64',
#              'Fish': 'float64', 'Cereals': 'float64', 'Starch': 'float64', 'Nuts': 'float64', 'Fruits & Vegetables': 'float64'}


dtype_dic_83 = {'date': 'str', 'Dow Jones Industrial Average': 'float64', '1 year moving average': 'float64'}
column_dictionary['83'] = dtype_dic_83

dtype_dic_84 = {'Temperature(K)': 'float64', 'Pressure(Liquid)': 'float64', 'Temperature(K)': 'float64', 'Pressure(Gas)': 'float64'}
column_dictionary['84'] = dtype_dic_84

# too long data headers
# dtype_dic_85 = {'gene': 'str','fetal_lung': 'float64', '232-97_SCC': 'float64', '232-97_node': 'float64', '68-96_Adeno': 'float64', '11-00_Adeno': 'float64', '69-96_Adeno': 'float64', '234-97_Adeno': 'float64', '319-00MT1_Adeno': 'float64', '319-00PT_Adeno': 'float64', '319-00MT2_Adeno': 'float64', '12-00_Adeno': 'float64', '237-97_Adeno': 'float64', '156-96_Adeno': 'float64', '157-96_SCC': 'float64', '320-00_Adeno_p': 'float64', '320-00_Adeno_c': 'float64', '161-96_Adeno': 'float64', '80-96_Adeno': 'float64', '239-97_SCC': 'float64', '75-95_combined': 'float64', '165-96_Adeno': 'float64',166-96_SCC,42-95_SCC,204-97_Adeno,245-97_SCC,245-97_node,58-95_SCC,132-95_Adeno,313-99PT_Adeno,313-99MT_Adeno,178-96_Adeno,246-97_SCC_p,246-97_SCC_c,180-96_Adeno,181-96_Adeno,184-96_Adeno,184-96_node,248-97_LCLC,185-96_Adeno,187-96_Adeno,191-96_Adeno,314-99_SCLC,314-99_normal,256-97_LCLC,257-97_Adeno,198-96_Adeno,315-99_SCLC,315-99_node,315-99_normal,137-96_Adeno,139-97_LCLC,207-97_SCLC,3-SCC,299-99_Adeno,199-97_Adeno_c,199-97_Adeno_p,6-00_LCLC,218-97_Adeno,219-97_SCC,219-97_normal,265-98_Adeno,220-97_SCC,220-97_node,222-97_Adeno,222-97_normal,306-99_Adeno,306-99_node,306-99_normal,223-97_Adeno,147-96_Adeno,59-96_SCC,226-97_Adeno,230-97_SCLC Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64',
            #  'Fish': 'float64', 'Cereals': 'float64', 'Starch': 'float64', 'Nuts': 'float64', 'Fruits & Vegetables': 'float64'}

# No headers
# dtype_dic_86 = {'Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64',
            #  'Fish': 'float64', 'Cereals': 'float64', 'Starch': 'float64', 'Nuts': 'float64', 'Fruits & Vegetables': 'float64'}
# first column name missing
dtype_dic_87 = {'SL_NO': 'int32', 'country': 'str', 'continent': 'str', 'year': 'int32', 'lifeExp': 'float64',
             'pop': 'float64', 'gdpPercap': 'str', 'iso_alpha': 'str', 'iso_num': 'int32'}

column_dictionary['87'] = dtype_dic_87


# dtype_dic_88 = {'Major Area': 'str', 'Regions': 'str', 'Country': 'str', 'Overall score': 'float64'}
# column_dictionary['88'] = dtype_dic_88
# # No headers
# # dtype_dic_89 = {'Country': 'str', 'Red Meat': 'float64', 'White Meat': 'float64', 'Eggs': 'float64', 'Milk': 'float64'}

# facing error while reading data: TypeError: Object dtype dtype('O') has no native HDF5 equivalent
# dtype_dic_90 = {'Major Area': 'str', 'Regions': 'str', 'Country': 'str', 'Overall score': 'float64'}
# column_dictionary['90'] = dtype_dic_90

# # No proper headers
# # dtype_dic_91 = {'Major Area': 'str', 'Regions': 'str', 'Country': 'str', 'Overall score': 'float64'}

# dtype_dic_92 = {'Time': 'str', 'Region': 'str', 'Level': 'str', 'Water Quality': 'str', 'Quantities of Exceed Standard': 'int32', 'Pollution Index': 'float64', 'Water Temp': 'float64', 'Ammonia Nitrogen(mg/L)': 'float64', 'Hosphorus(mg/L)': 'float64', 'Dissolved Oxygen(mg/L)': 'float64'}
# column_dictionary['92'] = dtype_dic_92
# # no headers
# # dtype_dic_93 = {'Major Area': 'str', 'Regions': 'str', 'Country': 'str', 'Overall score': 'float64'}

# # not present
# # dtype_dic_94 = {'Major Area': 'str', 'Regions': 'str', 'Country': 'str', 'Overall score': 'float64'}

dtype_dic_95 = {'Year': 'int32', 'Date': 'str', 'Temperature': 'int32'}
column_dictionary['95'] = dtype_dic_95

dtype_dic_96 = {'Quarter': 'str', 'Samsung': 'float64', 'Nokia/Microsoft': 'float64', 'Apple': 'float64', 'LG': 'float64', 'ZTE': 'float64', 'Huawei': 'float64'}
column_dictionary['96'] = dtype_dic_96

dtype_dic_97 = {'SL_NO': 'int32', 'IL (25°C)': 'float64', 'toluene (25°C)': 'float64', 'n-heptane (25°C)': 'float64'}
column_dictionary['97'] = dtype_dic_97

# # multiple csv file, not required at this moment
# # dtype_dic_98 = {'Major Area': 'str', 'Regions': 'str', 'Country': 'str', 'Overall score': 'float64'}

# # first column name not present
# # added SL_NO manually
dtype_dic_99 = {'SL_NO': 'int32', 'total_bill': 'float32', 'tip': 'float32', 'sex': 'str', 'smoker': 'str', 'day': 'str', 'time':'str', 'size': 'int32'}
column_dictionary['99'] = dtype_dic_99

dtype_dic_100 = {'Series': 'str', 'Wavelength': 'str', 'l position': 'int32', 'p position': 'int32'}
column_dictionary['100'] = dtype_dic_100


# Loop over folder names from 76 to 100
for folder_number in range(76, 101):
    if str(folder_number) not in column_dictionary:
        continue 

    folder_path = os.path.join(input_file_directory, str(folder_number))
    file_path = os.path.join(folder_path, "data.csv")
    
    # Check if the file exists, then read and save it
    if os.path.isfile(file_path):
        # Read the CSV file
        # df = pd.read_csv(file_path)
        # df = pd.read_csv(file_path, dtype=dtype_dic)
        df = pd.read_csv(file_path, dtype=column_dictionary[str(folder_number)])
        headers = df.columns.tolist()
        print('headers: ', headers)
        
        # h5_file = os.path.join(out_file_directory, f"{folder_number}_h5_data.h5")
        with h5py.File(os.path.join(out_file_directory, f"{folder_number}_h5_data.h5"), 'w') as h5file:  # Replace with your desired output file name
            # Step 3: Iterate over the columns and save each as a dataset
            # root_group = h5file.create_group('root')
            for header in headers:
                # root_group.create_dataset(header, data=df[header].values)
                h5file.create_dataset(header, data=df[header].values)


        # dataset_name = file_path.split('.')[0]
        # print('Read dataset name: ', dataset_name)
        # print('Header: ', df.head())
        # print('Country Column: ', df['Country'])  # Replace 'column_name' with your actual column name
        # print('First row: ', df.iloc[0])  # Prints the first row
        # print(df.iloc[0:25])  # Prints the first 10 rows


        # Define the output HDF5 file name using the folder name
        # h5_file = os.path.join(out_file_directory, f"{folder_number}_h5_data.h5")
        
        # Save to HDF5
        # df.to_hdf(h5_file, key='data', mode='w')
        # df.to_hdf(h5_file, key=dataset_name, mode='w')
        
        print(f"Saved {file_path} as {h5file}")
    else:
        print(f"File {file_path} does not exist.")
    
    # break
