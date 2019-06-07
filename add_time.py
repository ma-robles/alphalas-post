import numpy as np
import os.path
import glob 
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


myfiles = [] #list of image filenames
origin = input('Introduce ruta de la carpeta de origen.\nPor ejemplo: '
    'C:/Users/Invitado/Documentos/log_22nov17_105900\n ')
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
for i,name in enumerate(filenames):
    tname=name.split("_")[-1]
    filename=tname.split(".")[0]
    # Cambiar a formato XXhYYmZZs
    hour = filename[:2] + ':' + filename[2:4] + ':' + filename[4:]
    hours.append(hour)

#print(hours)
#print(filenames)
# graficar NO2_425-490.SlCol(NO2) y NO2_425-490.SlErr(NO2)
# eliminar negativos por nan

with open(output, 'w') as outfile:
    for i,line in enumerate(open(ruta)) :
        if i>1:
            #add time to data ! erase here?
            print(hours[i-2],line[:-2],sep="\t", file=outfile)

hms, no2, e_no2 = [], [], []
with open(output, 'r') as f:
    for line in f:
        #read no2_val
        no2_val = float(line.split('\t')[3]) / 1e17
        if no2_val > 0:
            hms.append(line.split('\t')[0])
            no2.append(no2_val)
            e_no2.append(float(line.split('\t')[2]) / 1e17)

fig, ax = plt.subplots(1,1)
plt.plot(hms, no2, lw=2)
plt.errorbar(hms, no2, yerr=e_no2, linestyle='None', lw=.7)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
plt.xticks(rotation=45)
plt.ylabel("No2.SlCol(NO2) (/1e17)")
plt.show()
