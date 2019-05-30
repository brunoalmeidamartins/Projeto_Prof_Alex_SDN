import matplotlib.pyplot as plt
import extrair_dados as ed

def calcula_media(vetor):
    media = 0.0
    for valor in vetor:
        media = media + valor
    return media/len(vetor)

matriz = ed.obtem_matriz_vazao()

x = [] #tempo
y1 = [] # h1_sem_qos
y2 = [] # h2_sem_qos
y3 = [] # h3_sem_qos

y4 = [] # h1_com_qos
y5 = [] # h2_com_qos
y6 = [] # h3_com_qos

y7 = [] # Media_Sem_QoS
y8 = [] # Media_Com_QoS

#Sem QoS
y1 = matriz[0]
y2 = matriz[1]
y3 = matriz[2]

#Com QoS
y4 = matriz[3]
y5 = matriz[4]
y6 = matriz[5]


vetores = [y1 , y2, y3, y4 ,y5, y6]
media_sem_qos = 0.0
media_com_qos = 0.0
j = 0
for vetor in vetores:
    if j < 3:
        media_sem_qos = media_sem_qos + calcula_media(vetor)
    else:
        media_com_qos = media_com_qos + calcula_media(vetor)
    j += 1

media_sem_qos = media_sem_qos/3
media_com_qos = media_com_qos/3

for i in range(0, len(y1)):
    x.append(i)
    y7.append(media_sem_qos)
    y8.append(media_com_qos)

fig,ax1 = plt.subplots()

#Sem QoS
ax1.plot(x,y1,'r-',linewidth=1.5,linestyle='-', label=u'Saída h1')
ax1.plot(x,y2,'g-',linewidth=1.5,linestyle='-', label=u'Saída h2')
ax1.plot(x,y3,'y-',linewidth=1.5,linestyle='-', label=u'Saída h3')
ax1.plot(x,y7,'b-',linewidth=1.5,linestyle='-', label=u'Média')
'''

#Com QoS
ax1.plot(x,y4,'r-',linewidth=1.5,linestyle='-', label=u'Saída h1')
ax1.plot(x,y5,'g-',linewidth=1.5,linestyle='-', label=u'Saída h2')
ax1.plot(x,y6,'y-',linewidth=1.5,linestyle='-', label=u'Saída h3')
ax1.plot(x,y8,'b-',linewidth=1.5,linestyle='-', label=u'Média')
'''

#Limites do grafico
ax1.set_ylim(0, 50)
ax1.set_xlim(0, 59) #O tempo correto eh 205


ax1.legend(loc='upper right') #Local das legendas

ax1.set_xlabel('Tempo(s)',fontsize=14)
ax1.set_ylabel('Megabits',fontsize=16)

plt.show()