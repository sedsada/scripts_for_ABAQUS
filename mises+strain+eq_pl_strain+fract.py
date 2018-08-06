from abaqusConstants import *
from odbAccess import *
import math
import numpy
import multiprocessing
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

print 'File '+FName+' has been created'
seOutputFile = open(FName,'w+')

def mylist (field):
   s=[]
   for j in range(len(field)):
      s.append(field[j].data)
   return s

start_time = time.time()

for i in range (F1,Fn,through):

   Ux = TheFrames[i].fieldOutputs['U'].getScalarField(componentLabel='U1')
   MisesField = TheFrames[i].fieldOutputs['S'].getScalarField(invariant=MISES)
   SDV4 = TheFrames[i].fieldOutputs['SDV4']
   SDV5 = TheFrames[i].fieldOutputs['SDV5']

   #second_time = time.time()
   #print 'Time_for_instance = ',second_time - start_time

   lists = []
   lists.append(mylist(MisesField.values)) #listMises = list[0]
   lists.append(mylist(SDV4.values))       #listMises = list[1]
   lists.append(mylist(SDV5.values))       #listMises = list[2]

   #third_time = time.time()
   #print 'Time_for_creation_lists = ', third_time - second_time

   pool = ThreadPool(3)

   AVG = pool.map(numpy.mean, lists)

   pool.close()
   pool.join()

   aveS = AVG[0] / 1000000
   aveSDV4 = AVG[1] *100
   aveSDV5 = AVG[2] *100

   seOutputFile.write(str(Ux.values[pnt].data*20000)+'    ')
   seOutputFile.write(str(aveS)+'    ')
   seOutputFile.write(str(aveSDV4) + '    ')
   seOutputFile.write(str(aveSDV5) + '   \n')

   #fourth_time = time.time()
   #print 'main_func = ', fourth_time - third_time

   print 'Frame ',int(str(i)),'  ex,%=',Ux.values[pnt].data*20000, '  Average Mises,MPa = ',aveS,'Average Fail ' \
                                                                                                 'Points,%=', \
      aveSDV4 ,'  Average eq_pl_strain,%=', aveSDV5

seOutputFile.close()
print 'Processing completed.  Runtime =', time.time() - start_time
