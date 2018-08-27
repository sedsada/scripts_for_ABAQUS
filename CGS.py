from abaqusConstants import *
from odbAccess import *
import math
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
import time

odbName = session.odbs.keys()[0]
odb = openOdb(path=odbName)

TheFrames = odb.steps['Step-1'].frames

pnt = int(getInput('The investigated point :'))
F1=int(getInput('N of the 1st frame:'))
Fn=int(getInput('N of the last frame:'))
through = int(getInput('Frequency:'))
FName = str(getInput('the Name of calculation:'))+'.dat'
Threads = int(getInput('Amount of threads :'))

print 'File '+FName+' has been created'
seOutputFile = open(FName,'w+')

begin_time = time.time()

def split_list(alist, wanted_parts=1):
   length = len(alist)
   return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
           for i in range(wanted_parts)]

temp_list = [i for i in range(Fn)]

lists = split_list(temp_list,wanted_parts=Threads)

def mylist (field):
   s=[]
   for j in range(len(field.values)):
      s.append(field.values[j].data)
   return s

def main_func(mainlist):
   for i in range (mainlist[0],len(mainlist)-1,through):

      Ux = TheFrames[i].fieldOutputs['U'].getScalarField(componentLabel='U1')
      MisesField = TheFrames[i].fieldOutputs['S'].getScalarField(invariant=MISES)
      SDV4 = TheFrames[i].fieldOutputs['SDV4']
      SDV5 = TheFrames[i].fieldOutputs['SDV5']

      aveS = np.mean(mylist(MisesField)) * 100000
      aveSDV4 = np.mean(mylist(SDV4)) *100
      aveSDV5 = np.mean(mylist(SDV5)) *100

      seOutputFile.write(str(Ux.values[pnt].data*20000)+'    ')
      seOutputFile.write(str(aveS)+'    ')
      seOutputFile.write(str(aveSDV4) + '    ')
      seOutputFile.write(str(aveSDV5) + '   \n')

begin_time = time.time()

pool = ThreadPool(Threads)
AVG = pool.map(main_func, lists)
pool.close()
pool.join()

seOutputFile.close()
print 'Processing completed.  Runtime =', time.time() - begin_time
