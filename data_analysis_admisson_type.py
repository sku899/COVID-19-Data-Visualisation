'''
plot admission types, all, emergence, planned 
'''
from pandas import read_csv
from pandas import to_datetime
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from matplotlib import rc


def check_data_contents(file_path, file_name):
    load_filename = file_path + '/' +file_name
    data = read_csv(load_filename)
    ##display first 20 records, check column names and dimension of data
    data['WeekEnding'] = data['WeekEnding'].apply(str)
    ##convert date string to date time (yy-mm-dd)
    data['WeekEnding']= to_datetime(data['WeekEnding'], format='%Y%m%d')
    peek = data.head(20)
    col_names = data.columns
    data_dim = data.shape
    print(peek)
    print(col_names)
    print(data_dim)
    return data
##
##    ##convert date (20200301, 20200302,.. etc) to string
##    data['Date'] = data['Date'].apply(str)
##    ##convert date string to date time (yy-mm-dd)
##    data['Date']= to_datetime(data['Date'], format='%Y%m%d')

def plotChart(ax1,plot_data,AdmissionType):
    plot_data2 =(plot_data['NumberAdmissions'].sub(plot_data['Average20182019']).div(plot_data['Average20182019'])).mul(100).to_frame('Percentage')
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
    if AdmissionType == 'Planned':
        ax1.tick_params(axis='x', labelbottom = True, bottom=True)
        ax1.set_xlabel('month')
        i=0
        ticks =[]
        ticklabels =[]
        for d in plot_data['WeekEnding']:
            if i % 2 ==0:
               ticks.append(i)
               ticklabels.append(d.strftime("%d/%b"))
            if i ==plot_data.shape[0]-1:
               ticks.append(i)
               ticklabels.append(d.strftime("%d/%b"))
            i = i+1
            print(i)
        ax2.set_xticks(ticks)
        ax2.set_xticklabels(ticklabels)
        print('xtick labels')
        print(ticklabels)
##        ax1.set_xticklabels()
##        print(ticklabels)
    else:
        ax1.tick_params(axis='x', labelbottom = False, bottom=True)
        ax2.set_xticks([])
        ax2.tick_params(axis='x', labelbottom = False, bottom=True)
        ax1.set_xticks([])
    ax1.tick_params(axis='y',  labelsize=8)
    ax2.tick_params(axis='y',  labelsize=8)
    ax1.set_ylabel('Number of Admissions', fontsize=8)
    ax2.set_ylabel('Percent Variation', fontsize=8)
##    ax1.set_title('Number of Admissions - All ages, sexes with Admission Type = ' +AdmissionType, fontsize=8,  verticala=lignment='center')
##    plt.title('Number of Admissions - All ages, sexes with '+ r'\textbf{' +AdmissionType +'} Admission' , fontsize=8)
    ax1.xaxis.set_label_position('top')
    ax1.set_xlabel('Number of Admissions - All ages, sexes with '+ r'$\bf{' +AdmissionType + '}$ '+' '+r'$\bf{ Admission' + '}$' , fontsize=8)
    ax1.xaxis.labelpad = 2
    # Solution for having two legends
    myl=lgnd1+[lgnd2]+[lgnd3]
    labs=[l.get_label() for l in myl]
    l = ax1.legend(myl, labs, loc='upper left', fontsize=6,  bbox_to_anchor=(0.26, 0.825, 0.735,0.15),mode = "expand", ncol = 3,framealpha=0.0)
    l.get_frame().set_linewidth(0) ##framealpha=0.0,
    ##ax1.set_ylim(0,max(sumdata['Total'])*0.825)
    ax1.set_ylim(0,40000)
    ax1.set_yticks([0,10000,20000,30000,40000])
    ax2_min=min( plot_data2['Percentage'])-10
    if ax2_min >-60:
        ax2_min=-60
    ax2.set_ylim(-90, 30)
    ax2.set_yticks([-90,-60,-30,0, 30])
    ax2.grid(axis='y',linestyle='dotted', color='green')
    ax1.grid(axis='y',linestyle='dotted', color='black')
    ##ax1.set_xlim(min(plot_data['WeekEnding']),max(plot_data['WeekEnding']))
    
            
    ##plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%b'))
    






## plotData function is to plot bar chart or line chart
def plotData(pos,plot_data, x_lim, y_lim, col="red"):
    plt.subplot(pos)
    print(plot_data.shape[1])
    num_of_col = plot_data.shape[1]
    show_x_ticks = (num_of_col == 3)
    if num_of_col == 3:
        print(plot_data.iloc[:,[0]])
        print(plot_data.columns[1])
        print(plot_data.dtypes,)
        plt.bar(plot_data.iloc[:,0],plot_data.iloc[:,1], \
                label = plot_data.columns[1], \
                color= 'blue')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
        plt.xticks(rotation=90, fontsize=8)
                
    plt.plot(plot_data.iloc[:,[0]], plot_data.iloc[:,[num_of_col-1]],\
             label = plot_data.columns[num_of_col-1], \
             color=col)
    ##change axis presentation
    plt.tick_params(bottom= show_x_ticks, labelbottom= show_x_ticks)    
    plt.xlim(x_lim[0], x_lim[1])
    plt.ylim(y_lim[0], y_lim[1])
    if pos<222:
        plt.ylabel('Number of Patients')
    if show_x_ticks:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2, tz=None))
        plt.xticks(rotation=90, fontsize=6)
    else:
        plt.xlabel('Date')
    plt.legend()
    
##import csv data file
    rc('text',usetext=True)
file_path ='./data';
file_name='hospital_admissions_hb_agesex_07102020.csv';
data = check_data_contents(file_path, file_name)
col_names = data.columns ##

##       'WeekEnding', 'HB', 'HBQF', 'AgeGroup', 'AgeGroupQF', 'Sex', 'SexQF',
##       'AdmissionType', 'AdmissionTypeQF', 'NumberAdmissions',
##       'Average20182019', 'PercentVariation'
## dimension of the file = 15059 x 12

for col_name in col_names:
    print(col_name)
    uniquevals = data[col_name].unique()
    print(uniquevals)
    
##filtering data
##only AgeGroup == 'All ages', Sex = 'All' and AdmissionType='All' extracted
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
data_aaa = data[(data.AgeGroup == 'All ages') & (data.Sex == 'All') &  \
               (data.AdmissionType == 'All')]
print(data_aaa.loc[:,['WeekEnding','Average20182019','NumberAdmissions' ]])
plot_data =data_aaa.groupby('WeekEnding')['Average20182019', 'NumberAdmissions'].sum().reset_index()



fig, axes = plt.subplots(3)
ax1=axes[0]
plotChart(ax1,plot_data,'All')

data_aae = data[(data.AgeGroup == 'All ages') & (data.Sex == 'All') &  \
               (data.AdmissionType == 'Emergency')]
plot_data =data_aae.groupby('WeekEnding')['Average20182019', 'NumberAdmissions'].sum().reset_index()
ax1=axes[1]
plotChart(ax1,plot_data,'Emergency')

data_aae = data[(data.AgeGroup == 'All ages') & (data.Sex == 'All') &  \
               (data.AdmissionType == 'Planned')]
plot_data =data_aae.groupby('WeekEnding')['Average20182019', 'NumberAdmissions'].sum().reset_index()
ax1=axes[2]
plotChart(ax1,plot_data,'Planned')
print('data size')
print(data.shape)
for col_name in col_names:
    print(col_name)
    uniquevals = data[col_name].unique()
    print(uniquevals)        
                
plt.show()




