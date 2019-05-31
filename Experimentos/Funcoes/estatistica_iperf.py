#!/usr/bin/python
#Aplicacao que reune diversas funcoes estatisticas - Versao 01/07/18

import sys
import math
import numpy as np
from matplotlib import pyplot as pl
from grafico import desenha
import extrair_dados as ed
#import seaborn as sns
#sns.set()
#Bruno



APROX = 2			#Numero de casas decimais para aproximacao

#Calculo da media
def media(L):
	soma=0.0
	for i in L:
		soma = soma + i
	return soma/len(L)

#Calculo da variancia
def variancia(L):
	soma=0.0
	x=media(L)
	for i in L:
		soma+=((i-x)**2)
	return soma/(len(L)-1)

#Calculo do desvio padrao
def desvioPadrao(L):
	return math.sqrt(variancia(L))

#Calculo do coeficiente de variacao
def cv(L):
	return desvioPadrao(L)/media(L)

#Calculo da covariancia
def covariancia(L1,L2):
	cov=0
	for i in range(len(L1)):
		cov+=(L1[i]-media(L1))*(L2[i]-media(L2))
	return cov

#Calculo da correlacao
def correlacao(L1,L2):
	return covariancia(L1,L2)/(desvioPadrao(L1)*desvioPadrao(L2))

#Calculo do intervalo de confianca
def ic(L,tabela):
	intervalo=[]
	x=media(L)
	erroPadrao=desvioPadrao(L)/math.sqrt(len(L))
	#tabela=raw_input('Digite o valor da tabela t/z para %d graus de liberdade: ' %(len(L)-1))
	liminf=x-(float(tabela)*erroPadrao)
	limsup=x+(float(tabela)*erroPadrao)
	intervalo.append(round(liminf,APROX))
	intervalo.append(round(limsup,APROX))
	return intervalo

#Calculo do Teste T
def icTesteT(L1,L2):
	intervalo=[]
	x1=media(L1)
	x2=media(L2)
	ep1=variancia(L1)/len(L1)
	ep2=variancia(L2)/len(L2)
	s=math.sqrt(ep1+ep2)
	numeradorv=(ep1+ep2)**2
	denominadorv=((ep1**2/(len(L1)+1))+(ep2**2/(len(L2)+1)))
	v=(numeradorv/denominadorv)-2
	tabela=input('Digite o valor da tabela t para %f graus de liberdade: ' %v)
	intervalo.append((x1-x2)-(float(tabela)*s))
	intervalo.append((x1-x2)+(float(tabela)*s))
	return intervalo

#Calculo das diferencas de amostras
def difAmostra(L1,L2):
	if len(L1)!=len(L2):
		print("Tamanhos de amostras diferentes")
		return
	dif=[]
	for i in range(len(L1)):
		dif.append(L1[i]-L2[i])
	return dif

#Calculo da regressao linear
def regressaoLinear(x,y):
	somatoriox = 0
	somatorioy = 0
	somatorioxy = 0
	somatoriox2 = 0
	SSY = 0
	somaestimate = 0
	somae = 0
	somae2 = 0

	n = len(x)						#Quantidade de amostras
	SS0 = n * media(y)**2					#Soma dos quadrados da media de y - SS0

	for i in range(n):
		somatoriox += x[i]				#Somatorio de x
		somatorioy += y[i]				#Somatorio de y
		somatorioxy += x[i] * y[i]			#Somatorio de x * y
		somatoriox2 += x[i]**2				#Soma dos quadrados de x
		SSY += y[i]**2					#Soma dos quadrados de y - SSY

	#Calculos das estimativas
	b1 = round((somatorioxy - n * media(x) * media(y)) / (somatoriox2 - n * (media(x)**2)),APROX)	#b1
	b0 = round(media(y) - (b1 * media(x)),APROX)							#b0

	for i in range(n):
		estimate = b0 + (b1 * x[i])			#Estimativa
		somaestimate += estimate			#Somatorio das estimativas
		e = y[i] - estimate				#Erro
		e2 = e**2					#Erro quadrado
		somae += e					#Soma dos erros
		somae2 += e2					#Soma dos erros quadrados

	SST = SSY - SS0						#Soma total dos quadrados - SST
	SSE = SSY - (b0 * somatorioy) - (b1 * somatorioxy)	#Soma dos erros quadrados (com regressao) - SSE

	#Calculos de R2 e Se
	R2 = 1 - (SSE / SST)					#Coeficiente de detelminacao - R2
	Se = math.sqrt(SSE / (n - 2))				#Desvio padrao de erros - Se

	#Calculos dos intervalos de confianca para regressoes
	Sb0 = round(Se * math.sqrt((1 / n) + (media(x)**2 / (somatoriox2 - (n * media(x)**2)))),APROX)
	Sb1 = round(Se / (math.sqrt(somatoriox2 - (n * media(x)**2))),APROX)

	tabela = float(input('Digite o valor da tabela t/z para %d graus de liberdade: ' %(n - 2)))

	b0min = b0 - tabela * Sb0				#Calculo dos intervalos de confianca
	b0max = b0 + tabela * Sb0
	b1min = b1 - tabela * Sb1
	b1max = b1 + tabela * Sb1

	#print 'Intervalo de confianca b0: %0.4f - %0.4f' %(b0min,b0max)
	#print 'Intervalo de confianca b1: %0.4f - %0.4f' %(b1min,b1max)

	#Calculos dos intervalos de confianca para predicoes
	xp = int(input('Digite o valor da amostra futura (Xp): '))
	m = 1
	yp = b0 + b1 * xp
	Sy = round(Se * math.sqrt((1 / m) + (1 / n) + (((xp - media(x))**2) / (somatoriox2 - (n * media(x)**2)))),APROX)

	ypmin = yp - tabela * Sy
	ypmax = yp + tabela * Sy
	#print 'Intervalo de confianca previsto (Yp): %0.4f - %0.4f' %(ypmin,ypmax)

	#Criacao dos graficos
	pl.title('Regressao Linear')
	pl.xlim(0,max(x)+1)
	pl.ylim(0,max(y)+1)

	pl.plot(x,y,'o')

	x2=np.array([min(x),max(x)])
	y2=np.array([media(y),media(y)])
	pl.plot(x2,b0+b1*x2,'-')				#Regressao
	pl.plot(x2,y2,'-')					#Media

	pl.text(max(x)+0.2,media(y),'y')
	pl.text(0.2,max(y),'y=%0.4f+%0.4fx' %(b0,b1))
	pl.text(0.2,max(y)-0.5,'R2: %0.4f' %R2)
	pl.text(0.2,max(y)-1.0,'Se: %0.4f' %Se)
	pl.text(0.2,max(y)-1.5,'e: %0.4f' %somae)
	pl.text(0.2,max(y)-2.0,'e2: %0.4f' %somae2)

	pl.show()

def converteBytesEmMegabits(vetor):#Recebe um vetor
    vet_aux = []
    for i in vetor:
        vet_aux.append(i*0.000008)
    return vet_aux

def converteBytesEmMegabyte(vetor):#Recebe um vetor
    vet_aux = []
    for i in vetor:
        vet_aux.append(i*0.000001)
    return vet_aux


#####Leitura de arquivos de resultados
#input = open('stp-16x4.txt', 'r')
#S5 = [float(foo) for foo in input.readlines()]
#input.close()

'''
############################################################################
Bruno TCC
############################################################################
'''

teste = '2Iperf' #SemIperf,1Iperf,2Iperf
cenario = '1' #1,2,3

#s1_tx1,s1_tx2,s1_tx3,s3_rx1,s3_rx2=vetores_estatistica('/home/bruno/ryu/Bruno/Resultados/Teste/Cenario'+cenario+'_'+teste+'.txt')

#h1_sem_QoS, h1_com_QoS = ed.obtem_vetores_ping()

SemQoS = True
Megabyte = True

if Megabyte:
	matriz = ed.obtem_matriz_iperf()
else:
	matriz = ed.obtem_matriz_vazao()

#Megabits
#s1_tx1 = converteBytesEmMegabits(s1_tx1)
#s1_tx2 = converteBytesEmMegabits(s1_tx2)
#s1_tx3 = converteBytesEmMegabits(s1_tx3)
#s3_rx1 = converteBytesEmMegabits(s3_rx1)
#s3_rx2 = converteBytesEmMegabits(s3_rx2)
'''
#Megabytes
s1_tx1 = converteBytesEmMegabyte(s1_tx1)
s1_tx2 = converteBytesEmMegabyte(s1_tx2)
s1_tx3 = converteBytesEmMegabyte(s1_tx3)
s3_rx1 = converteBytesEmMegabyte(s3_rx1)
s3_rx2 = converteBytesEmMegabyte(s3_rx2)
'''
#####Valores de tabelas T/Z
tam = len(matriz[0])

if tam > 30:
	tab = '1.96'
if tam == 30:
	tab = '2.045'
if tam == 25:
	tab = '2.064'
if tam == 20:
	tab = '2.093'
if tam == 15:
	tab = '2.145'



#tab='1.645'	#>30 90%
#tab='1.699'	#30 90%
#tab='1.711'	#25 90%
#tab='1.729'	#20 90%
#tab='1.761'	#15 90%

#####Medias
media_h1_sem_QoS=round(media(matriz[0]),APROX)
media_h2_sem_QoS=round(media(matriz[1]),APROX)
media_h3_sem_QoS=round(media(matriz[2]),APROX)

media_h1_com_QoS=round(media(matriz[3]),APROX)
media_h2_com_QoS=round(media(matriz[4]),APROX)
media_h3_com_QoS=round(media(matriz[5]),APROX)
#media_s1_tx3=round(media(s1_tx3),APROX)
#media_s3_rx1=round(media(s3_rx1),APROX)
#media_s3_rx2=round(media(s3_rx2),APROX)
'''
me5=round(media(E5),APROX)
me10=round(media(E10),APROX)
me15=round(media(E15),APROX)
me20=round(media(E20),APROX)
mt5=round(media(T5),APROX)
mt10=round(media(T10),APROX)
mt15=round(media(T15),APROX)
mt20=round(media(T20),APROX)
mi5=round(media(I5),APROX)
mi10=round(media(I10),APROX)
mi15=round(media(I15),APROX)
mi20=round(media(I20),APROX)
'''
#####Intervalos de Confianca
ic_h1_sem_qos=ic(matriz[0],tab)
ic_h2_sem_qos=ic(matriz[1],tab)
ic_h3_sem_qos=ic(matriz[2],tab)

ic_h1_com_qos=ic(matriz[3],tab)
ic_h2_com_qos=ic(matriz[4],tab)
ic_h3_com_qos=ic(matriz[5],tab)
#ic_s1_tx3=ic(s1_tx3,tab)
#ic_s3_rx1=ic(s3_rx1,tab)
#ic_s3_rx2=ic(s3_rx2,tab)

'''
ie5=ic(E5,tab)
ie10=ic(E10,tab)
ie15=ic(E15,tab)
ie20=ic(E20,tab)
it5=ic(T5,tab)
it10=ic(T10,tab)
it15=ic(T15,tab)
it20=ic(T20,tab)
ii5=ic(I5,tab)
ii10=ic(I10,tab)
ii15=ic(I15,tab)
ii20=ic(I20,tab)
'''
#####Impressao dos resultados
#h1_sem_QoS
print('\n\nMedia H1_Sem_QoS: '+str(media_h1_sem_QoS))
print('Desvio Padrao: '+str(round(desvioPadrao(matriz[0]),APROX)))
print('Variancia: '+str(round(variancia(matriz[0]),APROX)))
print('IC H1_Sem_QoS: '+str(ic_h1_sem_qos))

#h2_sem_QoS
print('\n\nMedia H2_Sem_QoS: '+str(media_h2_sem_QoS))
print('Desvio Padrao: '+str(round(desvioPadrao(matriz[1]),APROX)))
print('Variancia: '+str(round(variancia(matriz[1]),APROX)))
print('IC H2_Sem_QoS: '+str(ic_h2_sem_qos))

#h3_sem_QoS
print('\n\nMedia H3_Sem_QoS: '+str(media_h3_sem_QoS))
print('Desvio Padrao: '+str(round(desvioPadrao(matriz[2]),APROX)))
print('Variancia: '+str(round(variancia(matriz[2]),APROX)))
print('IC H3_Sem_QoS: '+str(ic_h3_sem_qos))


#h1_com_QoS
print('\n\nMedia H1_Com_QoS: '+str(media_h1_com_QoS))
print('Desvio Padrao: '+str(round(desvioPadrao(matriz[3]),APROX)))
print('Variancia: '+str(round(variancia(matriz[3]),APROX)))
print('IC H1_Com_QoS: '+str(ic_h1_com_qos))

#h2_com_QoS
print('\n\nMedia H2_Com_QoS: '+str(media_h2_com_QoS))
print('Desvio Padrao: '+str(round(desvioPadrao(matriz[4]),APROX)))
print('Variancia: '+str(round(variancia(matriz[4]),APROX)))
print('IC H2_Com_QoS: '+str(ic_h2_com_qos))

#h3_com_QoS
print('\n\nMedia H3_Com_QoS: '+str(media_h3_com_QoS))
print('Desvio Padrao: '+str(round(desvioPadrao(matriz[5]),APROX)))
print('Variancia: '+str(round(variancia(matriz[5]),APROX)))
print('IC H3_Com_QoS: '+str(ic_h3_com_qos))




"""
#EntradaIperf
print('\n\nMedia s3_rx2: '+str(media_s3_rx2))
print('Desvio Padrao: '+str(round(desvioPadrao(s3_rx2),APROX)))
print('Variancia: '+str(round(variancia(s3_rx2),APROX)))
print('IC s3_rx2: '+str(ic_s3_rx2))

#Saida Iperf 1
print('\n\nMedia s1_tx2: '+str(media_s1_tx2))
print('Desvio Padrao: '+str(round(desvioPadrao(s1_tx2),APROX)))
print('Variancia: '+str(round(variancia(s1_tx2),APROX)))
print('IC s1_tx2: '+str(ic_s1_tx2))

#Saida Iperf 2
print('\n\nMedia s1_tx3: '+str(media_s1_tx3))
print('Desvio Padrao: '+str(round(desvioPadrao(s1_tx3),APROX)))
print('Variancia: '+str(round(variancia(s1_tx3),APROX)))
print('IC s1_tx3: '+str(ic_s1_tx3))

"""












#####Geracao dos graficos
#if teste == 'SemIperf':
if SemQoS:
	#Sem QoS
	param1=[media_h1_sem_QoS, media_h2_sem_QoS, media_h3_sem_QoS]
	param2=[(ic_h1_sem_qos[1]-ic_h1_sem_qos[0])/2,
			(ic_h2_sem_qos[1]-ic_h2_sem_qos[0])/2,
			(ic_h3_sem_qos[1]-ic_h3_sem_qos[0])/2,
			]
	nome = 'Cenario '+cenario+' sem carga de trabalho'
	if Megabyte:
		desenha(param1,param2, 250,nome,'Iperf')
	else:
		desenha(param1, param2, 35, nome, 'Iperf1')
else:
	#Com QoS
	param1=[media_h1_com_QoS, media_h2_com_QoS, media_h3_com_QoS]
	param2=[(ic_h1_com_qos[1]-ic_h1_com_qos[0])/2,
			(ic_h2_com_qos[1]-ic_h2_com_qos[0])/2,
			(ic_h3_com_qos[1]-ic_h3_com_qos[0])/2,
			]
	nome = 'Cenario '+cenario+' sem carga de trabalho'
	if Megabyte:
		desenha(param1, param2, 250, nome, 'Iperf')
	else:
		desenha(param1, param2, 35, nome, 'Iperf1')



#elif teste == '1Iperf':
#	param1=[media_s3_rx1,media_s1_tx1,media_s3_rx2,media_s1_tx2]
#	param2=[(ic_s3_rx1[1]-ic_s3_rx1[0])/2,(ic_s1_tx1[1]-ic_s1_tx1[0])/2,(ic_s3_rx2[1]-ic_s3_rx2[0])/2,(ic_s1_tx2[1]-ic_s1_tx2[0])/2]
#	nome = 'Cenario '+cenario+' com uma carga de trabalho'
#	desenha(param1,param2, 5000,nome,teste)
#else:
#	param1=[media_s3_rx1,media_s1_tx1,media_s3_rx2,media_s1_tx2,media_s1_tx3]
#	param2=[(ic_s3_rx1[1]-ic_s3_rx1[0])/2,(ic_s1_tx1[1]-ic_s1_tx1[0])/2,(ic_s3_rx2[1]-ic_s3_rx2[0])/2,(ic_s1_tx2[1]-ic_s1_tx2[0])/2,(ic_s1_tx3[1]-ic_s1_tx3[0])/2]
#	nome = 'Cenario '+cenario+' com duas cargas de trabalho'
#	desenha(param1,param2, 8000,nome,teste)



'''
param1=[ms10,mt10,me10,mi10]
param2=[(is10[1]-is10[0])/2,(it10[1]-it10[0])/2,(ie10[1]-ie10[0])/2,(ii10[1]-ii10[0])/2]
desenha(param1,param2,200,'Trace 128 maps/4 reduces')
param1=[ms15,mt15,me15,mi15]
param2=[(is15[1]-is15[0])/2,(it15[1]-it15[0])/2,(ie15[1]-ie15[0])/2,(ii15[1]-ii15[0])/2]
desenha(param1,param2,200,'Trace 192 maps/16 reduces')
param1=[ms20,mt20,me20,mi20]
param2=[(is20[1]-is20[0])/2,(it20[1]-it20[0])/2,(ie20[1]-ie20[0])/2,(ii20[1]-ii20[0])/2]
desenha(param1,param2,350,'Trace 256 maps/16 reduces')
'''