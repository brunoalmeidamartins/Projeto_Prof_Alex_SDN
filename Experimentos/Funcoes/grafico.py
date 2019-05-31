#!/usr/bin/python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
#sn.set()


def desenha(y,ic,ymax,title, teste):
	color = '#9999ff'
	color1 = '#f8001d' #SaidaVideo
	color2 = '#1c8115' #SaidaIperf1
	color3 = '#bbc024' #SaidaIperf2
	teste = teste
	x = np.arange(len(y))
	bar_width = 0.5
	fonte = 13

	fig,ax = plt.subplots()

	if teste == 'SemIperf':
		ps,pt = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor(color)
		ps.set_edgecolor(color)
		pt.set_facecolor(color1)
		pt.set_edgecolor(color1)
		#ax.set_xticklabels([u'Entrada\nVídeo', u'Saida\nVídeo'],fontsize=fonte)
		ax.set_xticklabels([u'Sem QoS', u'Com QoS'], fontsize=fonte)
	elif teste == 'Iperf':
		ps,pt,pe = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor(color)
		ps.set_edgecolor(color)
		pt.set_facecolor(color)
		pt.set_edgecolor(color)
		pe.set_facecolor(color)
		pe.set_edgecolor(color)
		#ax.set_xticklabels([u'Entrada\nVídeo', u'Saída\nVídeo', 'Entrada\nIperf', u'Saída\nIperf 1'],fontsize=fonte)
		ax.set_xticklabels([u'h1\nOut', u'h2\nOut', u'h3\nOut'], fontsize=fonte)
	elif teste == 'Iperf1':
		ps,pt,pe = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor(color)
		ps.set_edgecolor(color)
		pt.set_facecolor(color)
		pt.set_edgecolor(color)
		pe.set_facecolor(color)
		pe.set_edgecolor(color)
		#ax.set_xticklabels([u'Entrada\nVídeo', u'Saída\nVídeo', 'Entrada\nIperf', u'Saída\nIperf 1'],fontsize=fonte)
		ax.set_xticklabels([u'h1\nOut', u'h2\nOut', u'h3\nOut'], fontsize=fonte)
	else:
		ps,pt,pe,pi,pa = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor(color)
		ps.set_edgecolor(color)
		pt.set_facecolor(color1)
		pt.set_edgecolor(color1)
		pe.set_facecolor(color)
		pe.set_edgecolor(color)
		pi.set_facecolor(color2)
		pi.set_edgecolor(color2)
		pa.set_facecolor(color3)
		pa.set_edgecolor(color3)
		#ax.set_xticklabels([u'Entrada\nVídeo', u'Saida\nVídeo', 'Entrada\nIperf', u'Saída\nIperf 1',u'Saída\nIperf 2'],fontsize=fonte)
		ax.set_xticklabels([u'Video\nIn', u'Video\nOut', 'iPerf\nIn', u'iPerf 1\nOut', u'iPerf 2\nOut'],fontsize=fonte)


	ax.set_xticks(x)
	ax.set_ylim([0,ymax])
	if teste == 'Iperf':
		ax.set_ylabel(u'Megabyte(MB)',fontsize=16)
	elif teste == 'Iperf1':
		ax.set_ylabel(u'Megabit(Mb)', fontsize=16)
	else:
		ax.set_ylabel(u'Megabyte(MB)', fontsize=16)
	ax.tick_params(axis='y',labelsize=13,right='off')
	ax.tick_params(axis='x',top='off')
	#ax.set_title(title,fontsize=18)

	plt.show()