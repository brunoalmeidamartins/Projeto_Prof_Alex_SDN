from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
#Pacotes
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
#Extras
from ryu.lib.dpid import dpid_to_str
from ryu.ofproto.ofproto_v1_2 import OFPG_ANY
from ryu.lib.mac import haddr_to_bin
#Topologia
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
#import networkx as nx
#Sistema
import os
import time
import requests
import pickle
from classe import Classe

import Tabela_IP_Porta as tb

IP_SERVIDOR = tb.ip_mac_servidor[0]

TABELA_IP_PORTAS = tb.tabela_ip_porta

TABELA_IP_SERVIDORES = tb.tabela_ip_servidores

MAC_SERVIDOR = tb.mac_servidor

BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'

ZERO_MAC = '00:00:00:00:00:00'

path_home = os.getenv("HOME") #Captura o caminho da pasta HOME

#Arquivos
filename = path_home+'/Projeto_Prof_Alex_SDN/classes.conf'	#Arquivo de lista de objetos Classe

class AppQoS(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(AppQoS, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.ip_to_mac = {}

    '''
    Eventos de Inicio de Topologia ou chegada de Switch
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        #Apaga regras do swithc
        [self.remove_flows(datapath, n) for n in [0, 1]]
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        #Regra de QoS de acordo com a tabela passada
        time.sleep(1)
        for regra in TABELA_IP_PORTAS:
            #os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_dst=' + regra[0] + ',nw_proto=17,tp_dst=' + regra[1] + ',actions=enqueue:' + regra[2] + ':' + self.filaQoS(regra[3]))
            #os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_dst=' + regra[0] + ',nw_proto=6,tp_dst=' + regra[1] + ',actions=enqueue:' + regra[2] + ':' + self.filaQoS(regra[3]))
            match1 = parser.OFPMatch(eth_type=0x0800,ipv4_dst=regra[0],ip_proto=6,tcp_dst=int(regra[1]))
            actions1 = [parser.OFPActionSetQueue(int(self.filaQoS(regra[3]))), parser.OFPActionOutput(port=7)]
            self.add_flow(datapath, 40000, match1, actions1, 0, 28)

        #Tudo que for TCP envia para o controlador
        match2 = parser.OFPMatch(eth_type=0x0800, ip_proto=6)
        self.add_flow(datapath, 1000, match2, actions, 0, 29)
        print('Eventos de Entradas Prontos!!!')

    '''
    FIM Eventos de Inicio de Topologia ou chegada de Switch
    '''

    '''
       Funcao de de Adicionar Regras
       '''

    def add_flow(self, datapath, priority, match, actions, idle_timeout=0, numero=0):
        print('Numero DEBUG: '+ str(numero))
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if idle_timeout == 0:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, idle_timeout=idle_timeout)
        datapath.send_msg(mod)

    '''
    Funcao de de Adicionar Regras
    '''




    '''
    Fila requerida para QoS
    '''
    def filaQoS(self, nome):
        # Acha qual fila eh a QoS pedida
        # Carregamento da lista de objetos Classe
        classlist = []
        if os.path.isfile(filename):
            filec = open(filename, 'rb')
            classlist = pickle.load(filec)
            filec.close()
        fila_saida = '0'  # Fila a ser aplicada
        for c in classlist:
            if c.nome == nome:
                fila_saida = c.id
        #print('Fila saida: ' + str(fila_saida))
        return str(fila_saida)

    '''
    FIM Fila requerida para QoS
    '''



    '''
    Area do Packet_In
    '''
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #Pega o id para saber o switch Openflow
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.ip_to_mac.setdefault(dpid, {})


        #Analisa os pacotes recebidos usando a biblioteca de pacotes.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth_pkt.dst
        src = eth_pkt.src

        #Obtem o numero da porta recebida da mensagem packet_in.
        in_port = msg.match['in_port']

        #aprende um endereco mac para evitar o FLOOD na proxima vez
        self.mac_to_port[dpid][src] = in_port



        # se o endereço MAC de destino já tiver sido aprendido,
        # decida qual porta enviar o pacote, caso contrário, FLOOD.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        # lista de acoes de construcao de regra.
        actions = [parser.OFPActionOutput(out_port)]

        #Aqui 1
        # Tipos de pacotes
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_udp = pkt.get_protocol(udp.udp)
        pkt_tcp = pkt.get_protocol(tcp.tcp)


        if pkt_arp: #arrumar a funcao
            # aprende o ip e o mac
            self.ip_to_mac[dpid][pkt_arp.src_ip] = [pkt_arp.src_mac, in_port] #Ex: {1: {'10.0.0.7': ['00:00:00:00:00:07', 7], '10.0.0.1': ['00:00:00:00:00:01', 1]}}
            #print(self.ip_to_mac)
            if pkt_arp.opcode == 1: #Arp Request
                print('Arp Request de ' + pkt_arp.src_ip + ' para ' + pkt_arp.dst_ip)
                #self.arp_reply(datapath, in_port, eth_pkt, pkt_arp, dpid)  # Responde o ARP

                if pkt_arp.dst_ip is self.ip_to_mac[dpid]:
                    self.arp_reply(datapath, in_port, eth_pkt, pkt_arp, dpid)  # Responde o ARP
                else: #Inunda a rede
                    out = parser.OFPPacketOut(datapath=datapath,
                                              buffer_id=ofproto.OFP_NO_BUFFER,
                                              in_port=in_port, actions=actions,
                                              data=msg.data)
                    datapath.send_msg(out)


            elif pkt_arp.opcode == 2: #Arp Reply
                print('Arp Reply de ' + pkt_arp.src_ip + ' para ' + pkt_arp.dst_ip)
                self.arp_reply(datapath, in_port, eth_pkt, pkt_arp, dpid) #Responde o ARP
            else:
                pass

        #if pkt_tcp and pkt_ipv4.src == IP_SERVIDOR:
        if pkt_tcp:
            vet_portas_servidor = []
            for linha in TABELA_IP_PORTAS:
                vet_portas_servidor.append(int(linha[1])) #Pega a posicao das portas da tabela
            if pkt_tcp.src_port in vet_portas_servidor:
                print('Pacote vindo do servidor')
                ofp = datapath.ofproto
                #match = parser.OFPMatch(eth_type='0x0800',in_port=in_port, ipv4_dst=pkt_ipv4.dst, tcp_dst=pkt_tcp.dst_port,)
                match = parser.OFPMatch(in_port=in_port,eth_type=0x0800,ipv4_src=pkt_ipv4.src, ipv4_dst=pkt_ipv4.dst,
                                        ip_proto=6,tcp_src=pkt_tcp.src_port,tcp_dst=pkt_tcp.dst_port)

                for regra in TABELA_IP_PORTAS:
                    if int(regra[1]) == pkt_tcp.src_port:
                        actions = [parser.OFPActionSetQueue(int(self.filaQoS(regra[3]))), parser.OFPActionOutput(port=self.mac_to_port[dpid][dst])]
                        self.add_flow(datapath, 1005, match, actions, 60, 27)
                        break
            else:
                match = parser.OFPMatch(in_port=in_port, eth_type=0x0800, ipv4_src=pkt_ipv4.src, ipv4_dst=pkt_ipv4.dst,
                                        ip_proto=6, tcp_src=pkt_tcp.src_port, tcp_dst=pkt_tcp.dst_port)
                actions = [parser.OFPActionOutput(port=self.mac_to_port[dpid][dst])]
                self.add_flow(datapath, 1005, match, actions, 60, 27)





        #Serve para demais regras que nao sao tcp
        # instala um fluxo no switch para evitar o packet_in na proxima vez
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions, 10)

        #Constroi o pacote de saida e envia

        #out = parser.OFPPacketOut(datapath=datapath,
        #                          buffer_id=ofproto.OFP_NO_BUFFER,
        #                          in_port=in_port, actions=actions,
        #                          data=msg.data)
        #datapath.send_msg(out)
        #print('To aqui!! ' +str(in_port) )

    '''
    FIM Area do Packet_In
    '''

    '''
    Arp Reply
    '''
    def arp_reply(self, datapath, in_port, eth_pkt, arp_pkt, dpid):
        # Browse Target hardware adress from ip_to_mac table.
        target_hw_addr = self.ip_to_mac[dpid][arp_pkt.dst_ip][0]
        target_ip_addr = arp_pkt.dst_ip

        pkt = packet.Packet()
        # Create ethernet packet
        pkt.add_protocol(ethernet.ethernet(ethertype=eth_pkt.ethertype,
                                           dst=eth_pkt.src,
                                           src=target_hw_addr))
        # Create ARP Reply packet
        pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY,
                                 src_mac=target_hw_addr,
                                 src_ip=target_ip_addr,
                                 dst_mac=arp_pkt.src_mac,
                                 dst_ip=arp_pkt.src_ip))

        self._send_packet(datapath, in_port, pkt)

    '''
    FIM Arp Reply
    '''


    '''
    Apaga Regras Swithc
    '''
    def remove_flows(self, datapath, table_id):
        """Removing all flow entries."""
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        empty_match = parser.OFPMatch()
        instructions = []
        flow_mod = self.remove_table_flows(datapath, table_id,
                                           empty_match, instructions)
        # print "deleting all flow entries in table ", table_id
        datapath.send_msg(flow_mod)


    def remove_table_flows(self, datapath, table_id, match, instructions):
        """Create OFP flow mod message to remove flows from table."""
        ofproto = datapath.ofproto
        flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, table_id,
                                                      ofproto.OFPFC_DELETE, 0, 0,
                                                      1,
                                                      ofproto.OFPCML_NO_BUFFER,
                                                      ofproto.OFPP_ANY,
                                                      OFPG_ANY, 0,
                                                      match, instructions)
        return flow_mod


    '''
    FIM Apaga Regras Swithc
    '''

    '''
    Envia Pacote para Host
    '''
    def _send_packet(self, datapath, port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt.serialize()
        # self.logger.info("packet-out %s" % (pkt,))
        data = pkt.data
        actions = [parser.OFPActionOutput(port=port)]
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=ofproto.OFPP_CONTROLLER,
                                  actions=actions,
                                  data=data)
        datapath.send_msg(out)


    '''
    FIM Envia Pacote para Host
    '''
'''
Tudo o que eu quiser iniciar, basta colocar aqui!!
'''
# Require
#app_manager.require_app('ryu.app.ofctl_rest')
#app_manager.require_app('ryu.app.simple_switch_13_mod')
#app_manager.require_app('ryu.app.simple_switch_13')
#app_manager.require_app('ryu.app.rest_conf_switch')
#app_manager.require_app('ryu.app.rest_topology')
# app_manager.require_app('ryu.app.rest_qos_mod')