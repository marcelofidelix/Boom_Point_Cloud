import math

#Comprimentos
d1 = 400
d2 = 1000
d3 = d2
d4 = 500

c1 = 2000
c2 = 1500
c3 = c2
c4 = 500

L1 = 5000
L2 = 20000
L3 = 5000

#Ângulos
alfa = math.atan(abs(d2 - d1) / (2 * L1))
beta = math.atan(abs(c1 - c2) / (2 * L1))
gama = math.atan(abs(d3 - d4) / (2 * L3))
delta = math.atan(abs(c3 - c4) / (2 * L3))

L = L1 + L2 + L3

#Número de subdivisões
n_pe = 5
n_in = 20
n_po = 5

#Passos
p_pe = L1 / n_pe
p_in = L2 / n_in
p_po = L3 / n_po

#Gera pontos
x = []
y = []
z = []

##########
#Seção pé#
##########
for i in range(n_pe + 1):
    x.append(i * p_pe)
    y.append(d1 / 2 + x[i] * math.sin(alfa))
    z.append(c1 / 2 - x[i] * math.sin(beta))
    
#Força os últimos valores de y e z para serem iguais a c2/2 e c2/2
y[-1] = d2/2
z[-1] = c2/2

# Replica os resultados para os 4 casos possíveis
def neg(l):
    temp = []
    for el in l:
        temp.append(-el)
    return temp

x = 4*x
y = y + neg(y) + y + neg(y)
z = neg(z) + z + z + neg(z)

#####################
#Seção intermediária#
#####################

x1 = []
y1 = []
z1 = []

for i in range(n_in + 1):
    x1.append(L1 + i * p_in)
    y1.append(d2 / 2)
    z1.append(c2 / 2)

x1 = 4*x1
y1 = y1 + neg(y1) + y1 + neg(y1)
z1 = neg(z1) + z1 + z1 + neg(z1)

#Elimina duplicidade de pontos na transição entre as seções
x1, y1, z1 = x1[1:], y1[1:], z1[1:]

#############
#Seção ponta#
#############

x2 = []
y2 = []
z2 = []

for i in range(n_po + 1):
    x2.append(L1 + L2 + i * p_po)
    y2.append(d3 / 2 - (x2[i] - L1 - L2) * math.sin(gama))
    z2.append(c3 / 2 - (x2[i] - L1 - L2) * math.sin(delta))
    
x2 = 4*x2
y2 = y2 + neg(y2) + y2 + neg(y2)
z2 = neg(z2) + z2 + z2 + neg(z2)

#Elimina duplicidade de pontos na transição entre as seções
x2, y2, z2 = x2[1:], y2[1:], z2[1:]

xf = x + x1 + x2
yf = y + y1 + y2
zf = z + z1 + z2

f = open('coord.txt','w')
s = ''
for i in range(len(xf)):
    s += str(xf[i]) + ',' + str(yf[i]) + ',' + str(zf[i]) + '\n'
f.write(s)
f.close()