import re
import pandas as pd
''' PING '''
def __dados_ping(path_arquivo):
    arq = open(path_arquivo, 'r')
    texto = arq.readlines()
    linha = (texto[len(texto) -1])
    vet = linha.split('/')
    dado = float(vet[4])
    return dado

def obtem_vetores_ping():
    path_projeto_ping_comQos = '/home/bruno/Projeto_Prof_Alex_SDN/Experimentos/Dados/Medida_RTT_Ping/Com_QoS/'
    path_projeto_ping_semQos = '/home/bruno/Projeto_Prof_Alex_SDN/Experimentos/Dados/Medida_RTT_Ping/Sem_QoS/'


    vet_avg_ping_ComQoS = []
    vet_avg_ping_SemQoS = []
    for i in range(0, 30):
        vet_avg_ping_ComQoS.append(__dados_ping(path_projeto_ping_comQos +'rtt_h1_srv1_'+str(i+1)+'.txt'))
        vet_avg_ping_SemQoS.append(__dados_ping(path_projeto_ping_semQos +'rtt_h1_srv1_'+str(i+1)+'.txt'))

    return vet_avg_ping_SemQoS, vet_avg_ping_ComQoS

''' iPerf '''

def __dadosIperf(path_arquivo):
    #print(path_arquivo)
    #path_h1 = path_caminho + 'h1/teste'
    #path_h2 = path_caminho + 'h3/teste'
    #path_h3 = path_caminho + 'h3/teste'
    arq = open(path_arquivo, 'r')
    texto = arq.readlines()
    i = 0
    vet_aux = []
    for linha in texto:
        if i > 5 and i < 66:
            vet = linha.split('sec')
            vet = vet[1].split(' ')
            if vet[2] == '':
                if vet[4] == 'KBytes':
                    vet_aux.append(float(vet[3]) * 0.001) #Transformando em Mbytes
                else:
                    vet_aux.append(float(vet[3]))
            else:
                if vet[3] == 'KBytes':
                    vet_aux.append(float(vet[2]) * 0.001) #Transformando em Mbytes
                else:
                    vet_aux.append(float(vet[2]))
        i += 1
    total_MBytes = 0.0
    for i in vet_aux:
        total_MBytes = total_MBytes + i
    return total_MBytes

def obtem_matriz_iperf():
    path_projeto_iperf_comQoS = '/home/bruno/Projeto_Prof_Alex_SDN/Experimentos/Dados/Medidas_Com_QoS/'
    path_projeto_iperf_semQoS = '/home/bruno/Projeto_Prof_Alex_SDN/Experimentos/Dados/Medidas_Sem_QoS/'
    h1_comQoS = []
    h2_comQoS = []
    h3_comQoS = []
    h1_semQoS = []
    h2_semQoS = []
    h3_semQoS = []
    for i in range(0, 30):
        h1_comQoS.append(__dadosIperf(path_projeto_iperf_comQoS+'h1/teste'+str(i+1)+'.txt'))
        h2_comQoS.append(__dadosIperf(path_projeto_iperf_comQoS+'h2/teste'+str(i+1)+'.txt'))
        h3_comQoS.append(__dadosIperf(path_projeto_iperf_comQoS+'h3/teste'+str(i+1)+'.txt'))

        h1_semQoS.append(__dadosIperf(path_projeto_iperf_semQoS + 'h1/teste' + str(i + 1) + '.txt'))
        h2_semQoS.append(__dadosIperf(path_projeto_iperf_semQoS + 'h2/teste' + str(i + 1) + '.txt'))
        h3_semQoS.append(__dadosIperf(path_projeto_iperf_semQoS + 'h3/teste' + str(i + 1) + '.txt'))
    matriz = [h1_semQoS, h2_semQoS, h3_semQoS, h1_comQoS, h2_comQoS, h3_comQoS]
    return matriz

def __vetor_vazao(path_arquivo):
    arq = open(path_arquivo, 'r')
    texto = arq.readlines()
    i = 0
    vet_aux = []
    for linha in texto:
        if i > 5 and i < 66:
            vet = linha.split('sec')
            vet = vet[1].split(' ')
            if vet[len(vet)-1] == 'Kbits/':
                vet_aux.append(float(vet[len(vet)-2]) * 0.001)
            elif vet[len(vet)-1] == 'bits/':
                vet_aux.append(float(vet[len(vet) - 2]) * 0.000001)
            else:
                vet_aux.append(float(vet[len(vet)-2]))
        i += 1
    return vet_aux


def __retorna_vetor_avg_matriz(matriz):
    db = pd.DataFrame(matriz)
    vet_retorno = []
    for i in range(0, 60):
        vet_retorno.append(db[i].mean())
    return vet_retorno


def obtem_matriz_vazao():
    path_projeto_iperf_comQoS = '/home/bruno/Projeto_Prof_Alex_SDN/Experimentos/Dados/Medidas_Com_QoS/'
    path_projeto_iperf_semQoS = '/home/bruno/Projeto_Prof_Alex_SDN/Experimentos/Dados/Medidas_Sem_QoS/'
    matriz_h1_comQoS = []
    matriz_h2_comQoS = []
    matriz_h3_comQoS = []

    matriz_h1_semQoS = []
    matriz_h2_semQoS = []
    matriz_h3_semQoS = []

    matriz_vazao = []

    for i in range(0, 30):
        matriz_h1_semQoS.append(__vetor_vazao(path_projeto_iperf_semQoS + 'h1/teste'+str(i+1)+'.txt'))
        matriz_h2_semQoS.append(__vetor_vazao(path_projeto_iperf_semQoS + 'h2/teste'+str(i+1)+'.txt'))
        matriz_h3_semQoS.append(__vetor_vazao(path_projeto_iperf_semQoS + 'h3/teste'+str(i+1)+'.txt'))

        matriz_h1_comQoS.append(__vetor_vazao(path_projeto_iperf_comQoS + 'h1/teste' + str(i + 1) + '.txt'))
        matriz_h2_comQoS.append(__vetor_vazao(path_projeto_iperf_comQoS + 'h2/teste' + str(i + 1) + '.txt'))
        matriz_h3_comQoS.append(__vetor_vazao(path_projeto_iperf_comQoS + 'h3/teste' + str(i + 1) + '.txt'))

    matriz_vazao.append(__retorna_vetor_avg_matriz(matriz_h1_semQoS))
    matriz_vazao.append(__retorna_vetor_avg_matriz(matriz_h2_semQoS))
    matriz_vazao.append(__retorna_vetor_avg_matriz(matriz_h3_semQoS))

    matriz_vazao.append(__retorna_vetor_avg_matriz(matriz_h1_comQoS))
    matriz_vazao.append(__retorna_vetor_avg_matriz(matriz_h2_comQoS))
    matriz_vazao.append(__retorna_vetor_avg_matriz(matriz_h3_comQoS))

    return matriz_vazao




#matriz = obtem_matriz_iperf()

#print(matriz)
#matriz = obtem_matriz_vazao()

#for vetor in matriz:
#    print(vetor)
#    print('')