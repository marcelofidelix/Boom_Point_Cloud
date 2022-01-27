#!/usr/bin/env python3
import pandas as pd
import pdb

p1 = '''
#!/usr/bin/env python
###
### This file is generated automatically by SALOME v9.4.0 with dump python functionality
###
import sys
import salome
salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/marcelofidelix')
###
### GEOM component
###
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
geompy = geomBuilder.New()
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
'''

p2 = ''

p3 = '''
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
'''

p4 = ''
p5 = ''

p6 = '''
if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
'''

f = open('coord.txt', 'r')
s = f.read()
f.close()

l = s.split('\n')
l = [el for el in l if el != '']

#Elimina duplicidades nos pontos
l = list(dict.fromkeys(l))

df = pd.DataFrame({'coords':l})
df = df['coords'].str.split(',', expand=True)
for col in df.columns.tolist():
	df[col] = pd.to_numeric(df[col])

def corda(v1, v2):
	if v1 > 0 and v2 > 0:
		return 'SD'
	if v1 > 0 and v2 < 0:
		return 'SE'
	if v1 < 0  and v2 > 0:
		return 'ID'
	else:
		return 'IE'

df['corda'] = df.apply(lambda x: corda(x[1], x[2]), axis=1)


#pdb.set_trace()

for i in range(len(l)):
	p2 += 'Vertex_'+str(i)+' = geompy.MakeVertex('+l[i].replace(' ', ',')+')'+'\n'

for i in range(len(l)):
	s = df.iloc[i]['corda']
	p4 += 'geompy.addToStudy('+ ' Vertex_' + str(i) + ", " + "'" + s+str(i)+"' )" + '\n'

for i in range(len(l)-1):
	s1 = df.iloc[i]['corda']
	s2 = df.iloc[i+1]['corda']
	if s1 == s2:
		p5 += 'Line_' + str(i) + ' = geompy.MakeLineTwoPnt('+ ' Vertex_' + str(i) + ',' + ' Vertex_' + str(i+1) + ")" + '\n'
	
for i in range(len(l)-1):
	s1 = df.iloc[i]['corda']
	s2 = df.iloc[i+1]['corda']
	if s1 == s2:
		p5 += 'geompy.addToStudy('+ ' Line_' + str(i) + ", 'Line_" + str(i) + "' )" + '\n'

file_content = p1 + p2 + p3 + p4 + p5 + p6

f = open('script_salome.py', 'w')

f.write(file_content)

f.close()
