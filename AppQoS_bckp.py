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


TABELA_IP_PORTAS = tb.tabela_ip_porta

TABELA_IP_SERVIDORES = tb.tabela_ip_servidores

MAC_SERVIDOR = tb.mac_servidor

path_home = os.getenv("HOME") #Captura o caminho da pasta HOME

#Arquivos
filename = path_home+'/Projeto_Prof_Alex_SDN/classes.conf'	#Arquivo de lista de objetos Classe

class AppQoS(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(AppQoS, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        #self.topology_api_app = self
        #self.net=nx.DiGraph()
        #self.nodes = {}
        #self.links = {}
        #self.no_of_nodes = 0
        #self.no_of_links = 0

    '''
    Eventos de Inicio de Topologia ou chegada de Switch
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        """Handle switch features reply to remove flow entries in table 0 and 1."""
        #msg = ev.msg
        #datapath = msg.datapath
        '''
        Apaga Regras do switch
        '''
        #[self.remove_flows(datapath, n) for n in [0, 1]]
        '''
        Fim Apaga Regras
        '''

        #Regra de Packet IN
        #ofproto = datapath.ofproto
        #parser = datapath.ofproto_parser
        #actions = [parser.OFPActionOutput(port=ofproto.OFPP_CONTROLLER,
        #                                  max_len=ofproto.OFPCML_NO_BUFFER)]
        #inst = [parser.OFPInstructionActions(type_=ofproto.OFPIT_APPLY_ACTIONS,
        #                                     actions=actions)]
        # match = parser.OFPMatch()
        #mod = parser.OFPFlowMod(datapath=datapath,
        #                        priority=0,
        #                        match=parser.OFPMatch(),
        #                        instructions=inst)
        #datapath.send_msg(mod)
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        #Regra de QoS de acordo com a tabela passada
        time.sleep(5)
        for regra in TABELA_IP_PORTAS:
            os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_dst=' + regra[0] + ',nw_proto=17,tp_dst=' + regra[1] + ',actions=enqueue:' + regra[2] + ':' + self.filaQoS(regra[3]))
            #os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_src='+ regra[0] +',nw_dst=' + regra[1] + ',nw_proto=6,tp_dst='+ regra[2] +',actions=enqueue:' + regra[3] + ':' + self.filaQoS(regra[4]))
            #os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_src='+ regra[1] +',nw_dst=' + regra[0] + ',nw_proto=6,tp_dst='+ regra[2] +',actions=enqueue:' + TABELA_IP_SERVIDORES[1] + ':' + self.filaQoS(regra[4]))
            #os.system('ovs-ofctl add-flow s1 priority=1,,dl_type=0x0800,in_port='+ regra[2] +',dl_src='+ regra[0] +',dl_dst=' + regra[1] + ',actions=enqueue:' + regra[2] + ':' + self.filaQoS(regra[3]) +',output:'+ regra[2])
            #os.system('ovs-ofctl add-flow s1 priority=1,dl_type=0x0800,in_port='+ MAC_SERVIDOR[1] +',dl_src='+ regra[1] +',dl_dst=' + regra[0] + ',actions=enqueue:' + MAC_SERVIDOR[1] + ':' + self.filaQoS(regra[3])+',output:'+ MAC_SERVIDOR[1])
        #for regra in TABELA_IP_SERVIDORES:
            #os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_dst=' + regra[0] + ',nw_proto=6,actions=enqueue:' + regra[1] + ':' + self.filaQoS(regra[2]))
            #os.system('ovs-ofctl add-flow s1 priority=40000,dl_type=0x0800,nw_dst=' + regra[0] + ',nw_proto=6,tp_dst=' + regra[1] + ',actions=enqueue:' + regra[2] + ':' + self.filaQoS(regra[3]))
    '''
    FIM Eventos de Inicio de Topologia ou chegada de Switch
    '''

    '''
       Funcao de de Adicionar Regras
       '''

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
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
        print('Fila saida: ' + str(fila_saida))
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

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        # Tipos de pacotes
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_udp = pkt.get_protocol(udp.udp)

    '''
    FIM Area do Packet_In
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