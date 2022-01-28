#!/usr/bin/env python3
#from unittest.case import DIFF_OMITTED
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
df = df.sort_values(0)
df['cont'] = df.groupby('corda').cumcount().astype(str)
df['cordaid'] = df['corda'] + df['cont']
df = df.drop('cont', 1)
#df = df.reset_index(drop=True)

df[0], df[1], df[2] = df[0].astype(str), df[1].astype(str), df[2].astype(str)
df['coord_str'] = df[0] +','+ df[1] +','+ df[2]

#Dataframes individuais com os elementos de cada corda
df_id = df[df['corda'] == 'ID'].reset_index(drop=True)[::2]
df_sd = df[df['corda'] == 'SD'].reset_index(drop=True)[1::2]
df_se = df[df['corda'] == 'SE'].reset_index(drop=True)[::2]
df_ie = df[df['corda'] == 'IE'].reset_index(drop=True)[1::2]

#Dataframes individuais com os elementos alternados de cada lateral
ld = pd.concat([df_id, df_sd]).sort_index()
superior = pd.concat([df_sd, df_se]).sort_index()
le = pd.concat([df_se, df_ie]).sort_index()
inferior = pd.concat([df_ie, df_id]).sort_index()

#pdb.set_trace()

for i in range(len(l)):
	s = df.iloc[i]['cordaid']
	p2 += s+' = geompy.MakeVertex('+df.iloc[i]['coord_str']+')'+'\n'

for i in range(len(l)):
	s = df.iloc[i]['cordaid']
	p4 += 'geompy.addToStudy('+ s + ", " + "'" + s+"' )" + '\n'

df_id_ = df[df['corda'] == 'ID'].reset_index(drop=True)
df_sd_ = df[df['corda'] == 'SD'].reset_index(drop=True)
df_se_ = df[df['corda'] == 'SE'].reset_index(drop=True)
df_ie_ = df[df['corda'] == 'IE'].reset_index(drop=True)

for i in range(len(df_id_)):
	try:
		p5 += 'Lineid_' + str(i) + ' = geompy.MakeLineTwoPnt('+ df_id_.iloc[i]['cordaid'] + ',' + df_id_.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ ' Lineid_' + str(i) + ', "' + ' Lineid_' + str(i) + '")' + '\n'
	except:
		continue
for i in range(len(df_sd_)):
	try:
		p5 += 'Linesd_' + str(i) + ' = geompy.MakeLineTwoPnt('+ df_sd_.iloc[i]['cordaid'] + ',' + df_sd_.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ ' Linesd_' + str(i) + ', "' + ' Linesd_' + str(i) + '")' + '\n'
	except:
		continue
for i in range(len(df_se_)):
	try:
		p5 += 'Linese_' + str(i) + ' = geompy.MakeLineTwoPnt('+ df_se_.iloc[i]['cordaid'] + ',' + df_se_.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ ' Linese_' + str(i) + ', "' + ' Linese_' + str(i) + '")' + '\n'
	except:
		continue
for i in range(len(df_ie_)):
	try:
		p5 += 'Lineie_' + str(i) + ' = geompy.MakeLineTwoPnt('+ df_ie_.iloc[i]['cordaid'] + ',' + df_ie_.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ ' Lineie_' + str(i) + ', "' + ' Lineie_' + str(i) + '")' + '\n'
	except:
		continue

#Lateral direita
for i, row in ld.iterrows():
	try:
		p5 += 'Lineld_' + str(i) + ' = geompy.MakeLineTwoPnt('+ ld.iloc[i]['cordaid'] + ',' + ld.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ 'Lineld_' + str(i) + ',"' + 'Lineld_' + str(i) +'")' + '\n'
	except:
		continue
#Superior
for i, row in ld.iterrows():
	try:
		p5 += 'Linesup_' + str(i) + ' = geompy.MakeLineTwoPnt('+ superior.iloc[i]['cordaid'] + ',' + superior.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ 'Linesup_' + str(i) + ',"' + 'Linesup_' + str(i) +'")' + '\n'
	except:
		continue
#Lateral esquerda
for i, row in ld.iterrows():
	try:
		p5 += 'Linele_' + str(i) + ' = geompy.MakeLineTwoPnt('+ le.iloc[i]['cordaid'] + ',' + le.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ 'Linele_' + str(i) + ',"' + 'Linele_' + str(i) +'")' + '\n'
	except:
		continue
#Inferior
for i, row in ld.iterrows():
	try:
		p5 += 'Lineinf_' + str(i) + ' = geompy.MakeLineTwoPnt('+ inferior.iloc[i]['cordaid'] + ',' + inferior.iloc[i+1]['cordaid'] + ")" + '\n'
		p5 += 'geompy.addToStudy('+ 'Lineinf_' + str(i) + ',"' + 'Lineinf_' + str(i) +'")' + '\n'
	except:
		continue

p5 += 'Linebase1 = geompy.MakeLineTwoPnt(ID0, SD0)' + '\n'
p5 += 'geompy.addToStudy(Linebase1, "Linebase1")' + '\n'
p5 += 'Linebase2 = geompy.MakeLineTwoPnt(SD0, SE0)' + '\n'
p5 += 'geompy.addToStudy(Linebase2, "Linebase2")' + '\n'
p5 += 'Linebase3 = geompy.MakeLineTwoPnt(SE0, IE0)' + '\n'
p5 += 'geompy.addToStudy(Linebase3, "Linebase3")' + '\n'
p5 += 'Linebase4 = geompy.MakeLineTwoPnt(IE0, ID0)' + '\n'
p5 += 'geompy.addToStudy(Linebase4, "Linebase4")' + '\n'

ponta = str(len(df_id_)-1)

p5 += 'Lineponta1 = geompy.MakeLineTwoPnt(ID'+ponta+', SD'+ponta+')' + '\n'
p5 += 'geompy.addToStudy(Lineponta1, "Lineponta1")' + '\n'
p5 += 'Lineponta2 = geompy.MakeLineTwoPnt(SD'+ponta+', SE'+ponta+')' + '\n'
p5 += 'geompy.addToStudy(Lineponta2, "Lineponta2")' + '\n'
p5 += 'Lineponta3 = geompy.MakeLineTwoPnt(SE'+ponta+', IE'+ponta+')' + '\n'
p5 += 'geompy.addToStudy(Lineponta3, "Lineponta3")' + '\n'
p5 += 'Lineponta4 = geompy.MakeLineTwoPnt(IE'+ponta+', ID'+ponta+')' + '\n'
p5 += 'geompy.addToStudy(Lineponta4, "Lineponta4")' + '\n'

#pdb.set_trace()

file_content = p1 + p2 + p3 + p4 + p5 + p6

f = open('script_salome.py', 'w')

f.write(file_content)

f.close()
