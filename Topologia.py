#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   autoSetMacs=True,
                   #autoStaticArp=True, #Define a tabela arp nos host automaticamente
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    srv1 = net.addHost('srv1', cls=Host, ip='10.0.0.7', defaultRoute=None)




    info( '*** Add links\n')
    net.addLink(h1, s1, 1, 1)
    net.addLink(h2, s1, 1, 2)
    net.addLink(h3, s1, 1, 3)
    net.addLink(h4, s1, 1, 4)
    net.addLink(h5, s1, 1, 5)
    net.addLink(h6, s1, 1, 6)
    net.addLink(srv1, s1, 1, 7)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])

    info('*** Setting routes\n')
    h1.cmd('route add default dev h1-eth1')
    h2.cmd('route add default dev h2-eth1')
    h3.cmd('route add default dev h3-eth1')
    h4.cmd('route add default dev h4-eth1')
    h5.cmd('route add default dev h5-eth1')
    h6.cmd('route add default dev h6-eth1')
    srv1.cmd('route add default dev srv1-eth1')

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

