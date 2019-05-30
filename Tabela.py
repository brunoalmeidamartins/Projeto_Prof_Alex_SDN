ip_servidor = '10.0.0.7'
mac_placa_servidor = '00:00:00:00:00:07'
porta_servidor = '"s1-eth7"'

ip_mac_servidor = [ip_servidor, mac_placa_servidor]
mac_servidor = [mac_placa_servidor, porta_servidor]

tabela_ip_porta = [
                   [ip_servidor, '2001', porta_servidor, 'Classe30Mb'],
                   [ip_servidor, '2002', porta_servidor, 'Classe30Mb_1'],
                   [ip_servidor, '2003', porta_servidor, 'Classe30Mb_2']
                  ]
tabela_ip_servidores = [ip_servidor, porta_servidor]