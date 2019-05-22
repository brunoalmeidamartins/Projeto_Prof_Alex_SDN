ip_servidor = '10.0.0.7'
mac_placa_servidor = '00:00:00:00:00:07'
porta_servidor = '"s1-eth7"'

ip_mac_servidor = [ip_servidor, mac_placa_servidor]
mac_servidor = [mac_placa_servidor, porta_servidor]

tabela_ip_porta = [
                   [ip_servidor, '2000', porta_servidor, 'Classe10Mb'],
                   [ip_servidor, '2001', porta_servidor, 'Classe10Mb'],
                   [ip_servidor, '2002', porta_servidor, 'Classe20Mb'],
                   [ip_servidor, '2003', porta_servidor, 'Classe20Mb'],
                   [ip_servidor, '2004', porta_servidor, 'Classe30Mb'],
                   [ip_servidor, '2005', porta_servidor, 'Classe30Mb'],
                   [ip_servidor, '2006', porta_servidor, 'Classe10Mb'],
                   [ip_servidor, '2007', porta_servidor, 'Classe10Mb'],
                   [ip_servidor, '2008', porta_servidor, 'Classe20Mb'],
                   [ip_servidor, '2009', porta_servidor, 'Classe20Mb'],
                   [ip_servidor, '2010', porta_servidor, 'Classe30Mb'],
                   [ip_servidor, '2011', porta_servidor, 'Classe30Mb'],
                   [ip_servidor, '2012', porta_servidor, 'Classe30Mb'],
                   [ip_servidor, '2013', porta_servidor, 'Classe100Mb'],
                   [ip_servidor, '2014', porta_servidor, 'Classe100Mb'],
                   [ip_servidor, '80', porta_servidor, 'Classe10Mb'],
                  ]
tabela_ip_servidores = [ip_servidor, porta_servidor]