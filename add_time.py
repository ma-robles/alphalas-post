import numpy as np
import os.path
import glob 
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import datetime as dt
from matplotlib.dates import DateFormatter
import solarPos as solar

sol=solar.solarPos(19.4, -99.149999, -6)
origin=sys.argv[1]
col_var=2
col_err=3
root=origin.split("/")[-1]
root=root.split("_")[0]
print(root)
input2=root+"colNO2.txt"
output=origin+"/"+root+"colno2.txt"
ruta=origin+"/"+input2
print("input2:",input2,)
print("output:",output)
print("ruta:  ",ruta)

# Para saber si el archivo existe. Si no, salimos del codigo.
if not os.path.isdir(origin):
    print('Invalid given path.')
    exit(1)

# Lista vacia para guardar las horas
hours = []
filenames=glob.glob(os.path.join(origin, '*.dat'))
filenames.sort() # inicia ordena pero no ordena numericamente bien
ifmt="%y%m%d_%H%M%S"
for i,name in enumerate(filenames):
    filename=name.split("/")[-1].split('.')[0]
    hours.append(dt.datetime.strptime(filename,ifmt))

#print(hours)
#print(filenames)
# graficar NO2_425-490.SlCol(NO2) y NO2_425-490.SlErr(NO2)
# eliminar negativos por nan

head='date\t'
with open(output, 'w') as outfile:
    for i,line in enumerate(open(ruta)) :
        #get data
        data=line.split('\t')
        if i==1:
            head+=data[col_var]+'\t'+data[col_err]
            print(head,file=outfile)
        if i>1:
            #add time & extract data cols  
            print(dt.datetime.strftime(hours[i-2],ifmt),
                data[col_var],data[col_err],
                sep="\t", 
                file=outfile,
                )

hms=np.array([])
no2=np.array([])
err=np.array([])
s_pos=np.array([])
plot_fmt = DateFormatter("%H:%M") 
with open(output, 'r') as f:
    for i,line in enumerate(f):
        if i==0:
            continue
        h=dt.datetime.strptime(line.split('\t')[0],ifmt)
        hms=np.append(hms, h)
        sol.calculate(h)
        s_pos=np.append(s_pos,sol.zen_cos)
        no2_val = float(line.split('\t')[1])
        no2=np.append(no2,no2_val)
        err=np.append(err,float(line.split('\t')[2]))

fig, ax = plt.subplots(2)
ax[0].plot(hms,no2)
no2_max=np.max(no2)
ax[0].plot(hms,s_pos*no2_max)
subs=15
ax[0].errorbar(hms[::subs], no2[::subs],
        yerr=err[::subs],
        fmt='gray',
        capsize=5,
        linestyle='None',
        #lw=.7,
        )
ax[1].plot(hms,s_pos*no2)
ax[1].errorbar(
        hms[::subs],
        no2[::subs]*s_pos[::subs],
        yerr=err[::subs]*s_pos[::subs],
        fmt='gray',
        capsize=5,
        linestyle='None',
        #lw=.7,
        )
for a in ax:
    a.label_outer()
lims=list(plt.axis())
#lims[2]=0
#plt.axis(lims)
#plt.xticks(rotation=45)
ax[1].xaxis.set_major_formatter(plot_fmt)
#plt.ylabel(head.split('\t')[1])
fig.suptitle(head.split('\t')[1])
plt.show()
