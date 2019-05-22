import matplotlib.pyplot as plt
arq = open('Medida_RTT/Pckt_32B/rtt_h1_2000.txt','r')
#arq = open('Medida_RTT/Pckt_32B/rtt_h2_2002.txt','r')
#arq = open('Medida_RTT/Pckt_32B/rtt_h3_2004.txt','r')
#arq = open('Medida_RTT/Pckt_32B/rtt_h4_5001.txt','r')

texto = arq.readlines()

arq.close()

i = 0
t = 0
vet_linhas = []
vet_x = []
for linha in texto:
    if i > 5 and i % 2 == 1 and i < len(texto) -1:
        vet_linhas.append(linha)
        vet_x.append(t)
        t += 1
    i += 1

vet_y = []
for linha in vet_linhas:
    linha = linha.split('/')[3]
    linha = linha.replace(' us\n','')
    vet_y.append(int(linha))

plt.plot(vet_x, vet_y)
plt.show()