'''
plot covid-19 averaged daily and 7 day average admitted number
plot week day average between 01/March/2020 and 21/Nov/2020
plot week day average between 23/March and 10/May/2020
'''
from pandas import read_csv
from pandas import to_datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


## plotData function is to plot bar chart or line chart
def plotData(pos,plot_data, x_lim, y_lim, col="red"):
    ax = plt.subplot(pos)
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
        plt.xticks(rotation=0, fontsize=8)
                
    plt.plot(plot_data.iloc[:,[0]], plot_data.iloc[:,[num_of_col-1]],\
             label = plot_data.columns[num_of_col-1], \
             color=col)
    ##change axis presentation
    plt.tick_params(bottom= show_x_ticks, labelbottom= show_x_ticks)    
    plt.xlim(x_lim[0], x_lim[1])
    plt.ylim(y_lim[0], y_lim[1])
    fontsize=8
    if pos<222:
        plt.ylabel('Admitted Number') #('No. of Patients')
    if show_x_ticks:
##        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
##        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2, tz=None))
        i=0
        ticks=[]
        for d in data['Date']:
            if i % 14==0:
                ticks.append(d)
            if i == data.shape[0]-1:
                ticks.append(d)
            i= i+1
        plt.xticks(ticks)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.xticks(rotation=90, fontsize=6)
    else:
        plt.xlabel('Date',fontsize=fontsize)
    
    if pos == 221:
        plt.title('COVID-19 Daily Admitted Number', fontsize=fontsize)
    if pos==222:
        plt.title('COVID-19 Seven-Day Average Admitted Number', fontsize=fontsize)
    if pos==212:
        ##plt.title('COVID-19 Daily Admitted Number & Seven-Day Average Admitted Number', fontsize=fontsize)
        ax.xaxis.set_label_position('top')
        ax.set_xlabel('COVID-19 Daily Admitted Number & Seven-Day Average Admitted Number', fontsize=fontsize)
        ax.xaxis.labelpad = 2
        dateindex = [22, 70, 106, 125, 157]
        dateindex = [22, 136,222]
        str_date=['Lockdown start','Stay alert', 'Reopen non-essential', 'Super Saturday','Reopen close-contact']
        str_date=['Lockdown(2303)','Phase III (1507)','Temporary measures (0910)' ]
        style = ['fuchsia','orange','aqua', 'b:', 'g:']  
        for i, dindex in enumerate(dateindex):
            plt.plot([data['Date'][dindex],data['Date'][dindex]],[0,250],color = style[i],label = str_date[i], linestyle='-.' )
        print('date')
        print(data['Date'][22])
        handles,labels = ax.get_legend_handles_labels()
        handles = [handles[0], handles[4], handles[1], handles[2], handles[3]]
        labels = [labels[0], labels[4],labels[1], labels[2], labels[3]]
        plt.plot([data['Date'][0], data['Date'][data.shape[0]-1]],[data['NumberAdmitted'][22],data['NumberAdmitted'][22]],'k--')
        
        plt.legend(handles,labels,fontsize=fontsize,loc='upper right')
        ##plt.legend(fontsize=fontsize, loc = 'upper right')
            
    
##import csv data file
file_path ='./data';
file_name='daily_covid_admissions_20201028.csv';
load_filename = file_path + '/' +file_name
data = read_csv(load_filename)
##display first 20 records, check column names and dimension of data
peek = data.head(20)
col_names = data.columns
##col_names =['Date', 'NumberAdmitted', 'SevenDayAverage', 'SevenDayAverageQF']
data_dim = data.shape
##dimension of data = 235 x 4
print(peek)
print(col_names)
print(data_dim)

##convert date (20200301, 20200302,.. etc) to string
data['Date'] = data['Date'].apply(str)
##convert date string to date time (yy-mm-dd)
data['Date']= to_datetime(data['Date'], format='%Y%m%d')
##plot_data=[data['Date'],data['SevenDayAverage'],data['NumberAdmitted']];
##set x and y axes' limitation
x_limit = [min(data['Date']),max(data['Date'])]
y_limit = [min(data['NumberAdmitted']),max(data['NumberAdmitted'])*1.1]
##first plot
##plotData(pos=221,plot_data = data.loc[:,['Date','NumberAdmitted']],\
##         x_lim = x_limit, y_lim = y_limit, \
##         col ='blue')
totalcount=[0,0,0,0,0,0,0]
numOfcount =[0,0,0,0,0,0,0]
currentPos=0
for num in data['NumberAdmitted']:
    totalcount[currentPos]=totalcount[currentPos]+num
    numOfcount[currentPos]=numOfcount[currentPos]+1
    currentPos = currentPos+1
    currentPos = currentPos % 7
for i, num in enumerate(totalcount):
    totalcount[i]= num/numOfcount[i]
plt.subplot(223)
plt.bar([1,2,3,4,5,6,7], totalcount, color='navy')
plt.xticks([1,2,3,4,5,6,7], ('Sun','Mon','Tue','Wed','Thu','Fri','Sat'),fontsize=6)    
plt.title('Week Day Average Admitted Number \n from 01/03 to 21/10',fontsize=8);
plt.ylim(0,40)
plt.ylabel('Admitted Number')
totalcount=[0,0,0,0,0,0,0]
numOfcount =[0,0,0,0,0,0,0]
currentPos=0
j=0
for num in data['NumberAdmitted']:
    if j>=22 and j<=70:
        totalcount[currentPos]=totalcount[currentPos]+num
        numOfcount[currentPos]=numOfcount[currentPos]+1
        print(j)
    j=j+1
    currentPos = currentPos+1
    currentPos = currentPos % 7
for i, num in enumerate(totalcount):
    totalcount[i]= num/numOfcount[i]
plt.subplot(224)
plt.bar([1,2,3,4,5,6,7], totalcount, color ='lightskyblue')
plt.xticks([1,2,3,4,5,6,7], ('Sun','Mon','Tue','Wed','Thu','Fri','Sat'),fontsize=6) 
plt.title('Week Day Average Admitted Number \n from 23/03 to 10/05',fontsize=8);
plt.ylim(0,120)
##second plot
##plotData(pos=222,plot_data = data.loc[:,['Date','SevenDayAverage']],\
##         x_lim = x_limit, y_lim = y_limit)
##third plot
fig = plt.figure ()
plotData(pos=212,plot_data = data.loc[:,['Date','NumberAdmitted','SevenDayAverage']],\
         x_lim = x_limit, y_lim = y_limit)
print('data size')
print(data.shape)
print('Data File Column Names:')
for cn in data.columns:
    print(cn)

print(data['SevenDayAverageQF'].unique())
plt.show()


