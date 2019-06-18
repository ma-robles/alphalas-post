import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def get_srfc_data(filename,day):
    '''
    get data from rama files
    filename - path of file
    day - plot day (dd/mm/yyyy)
    '''
    data=[]
    time=[]
    fmt='%d/%m/%Y %H:%M'
    for i,line in enumerate(open(filename,encoding='latin-1')):
        if i>10:
            data_str=line.split(',')
            if data_str[1]=='CCA' and data_str[2]=='NO2' and day in data_str[0] :
                try:
                    time.append(dt.datetime.strptime(data_str[0],fmt))
                except:
                    continue
                try:
                    conc=float(line.split(',')[3])
                except:
                    conc=float('nan')
                data.append(conc)
    return time,data

if __name__=='__main__':
    filename= sys.argv[1]
    plt.figure()
    time,data=get_srfc_data(filename, '20/03/2019')
    plt.plot(time,data)
    plt.show()
