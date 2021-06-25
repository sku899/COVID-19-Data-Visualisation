##import required packages
from pandas import read_csv
from pandas import to_datetime
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from matplotlib import rc

##define functions
def load_data(file_path, file_name):
    load_filename = file_path + '/' +file_name
    data = read_csv(load_filename)
    return data

def convert_to_datetime(data, pos_name):
    fmt = '%Y%m%d';
    if isinstance(pos_name, int):
        pos_name= data.columns[pos_name]
    data[pos_name] = data[pos_name].apply(str)
    ##convert date string to date time (yy-mm-dd)
    data[pos_name]= to_datetime(data[pos_name], format=fmt)
    return data


def check_data_struc(data, disp_all_column=False):  
    ##display first and last few records,
    ##check column names and dimension of data
    peek1 = data.head(5)
    peek2 = data.tail(5)
    header_names = data.columns
    data_dim = data.shape
    data_type = data.dtypes
    if disp_all_column:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
    print('first 5 records..........')
    print(peek1)
    time_len =5
    print(f'last {time_len} records...........')
    print(peek1)
    print('header names...........')
    print(header_names)
    print('data dimension',data_dim,sep =' = ')
    print('data types=', data_type)
    return header_names


def print_unique_values(header_names):
    for header_name in header_names:
        print(header_name)
        uniquevals = data[header_name].unique()
        print(uniquevals)


def plotChart(ax,plot_data,AdmissionType):
    sumdata= (plot_data['NumberAdmissions'].add(plot_data['Average20182019'])).to_frame('Total')
    ax2 = ax1.twinx()  # set up the 2nd axis
    barWidth = 0.475
    index = np.arange(plot_data.shape[0])
    lgnd3 = ax1.bar( index,plot_data['Average20182019'],alpha=0.4,width=barWidth, label='2018 & 2019 Average')
    lgnd2 = ax1.bar(index+barWidth*0.5, plot_data['NumberAdmissions'],\
            width=barWidth, alpha=0.8,label='2020 Weekly Admissions') #bottom = plot_data['Average20182019']
    lgnd1 = ax2.plot(index,plot_data2['Percentage'], 'r-o',label='Percent Variation',markersize=3)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax1.tick_params(axis='x', labelrotation=90, labelsize=8)

    
##read the data
file_path = './data';
file_name = 'hospital_admissions_hb_agesex_07102020.csv';
data = load_data(file_path, file_name)
data = convert_to_datetime(data, 0)
header_names = check_data_struc(data, disp_all_column = True)
print_unique_values(header_names)
##data types
##WeekEnding          datetime64[ns]
##HB                          object
##HBQF                        object
##AgeGroup                    object
##AgeGroupQF                  object
##Sex                         object
##SexQF                       object
##AdmissionType               object
##AdmissionTypeQF             object
##NumberAdmissions             int64
##Average20182019            float64
##PercentVariation           float64
## filtering data
date_col = 'WeekEnding'
average_an_col = 'Average20182019'
y2020_an_col = 'NumberAdmissions'
variation_col = 'Variation'

filtered_data = data[(data.AgeGroup == 'All ages') & (data.Sex == 'All') &  \
               (data.AdmissionType == 'All')]
plot_data = filtered_data.groupby(date_col)\
            [[average_an_col,y2020_an_col]].sum().reset_index()
plot_data[variation_col] = (plot_data[y2020_an_col].\
                  sub(plot_data[average_an_col]).\
                  div(plot_data[average_an_col])).\
                  mul(100).to_frame('Percentage')


