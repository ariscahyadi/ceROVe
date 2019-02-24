#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info, debug
from mininet.node import Host, RemoteController

QUAGGA_DIR = '/usr/lib/quagga'
# Must exist and be owned by quagga user (quagga:quagga by default on Ubuntu)
QUAGGA_RUN_DIR = '/var/run/quagga'
CONFIG_DIR = 'configs'


class LinuxRouter( Host ):

    def __init__(self, name, quaggaConfFile, zebraConfFile, intfDict, *args, **kwargs):
        Host.__init__(self, name, *args, **kwargs)

        self.quaggaConfFile = quaggaConfFile
        self.zebraConfFile = zebraConfFile
        self.intfDict = intfDict

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	self.cmd('/usr/lib/quagga/zebra -d -f %s -z %s/zebra%s.api -i %s/zebra%s.pid' % (self.zebraConfFile, QUAGGA_RUN_DIR, self.name, QUAGGA_RUN_DIR, self.name))
        self.cmd('/usr/lib/quagga/bgpd -d -f %s -z %s/zebra%s.api -i %s/bgpd%s.pid' % (self.quaggaConfFile, QUAGGA_RUN_DIR, self.name, QUAGGA_RUN_DIR, self.name))


    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
	self.cmd("ps ax | egrep 'bgpd%s.pid|zebra%s.pid' | awk '{print $1}' | xargs kill" % (self.name, self.name))
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):

    def build( self, **_opts ):

        #r1 = self.addNode( 'r1', cls=LinuxRouter, ip='192.168.1.1/24' )

	intfs = {'r1-eth0': {'ipAddrs': ['10.0.1.1/24'], 'mac': '00:88:00:00:00:01'},
                 'r1-eth1': {'ipAddrs': ['192.168.1.0/24']}}

	r1 = self.addHost('r1', cls=LinuxRouter,
                            intfDict=intfs,
                            quaggaConfFile='./quagga1.conf',
                            zebraConfFile='./zebra.conf')

 	#r2 = self.addNode( 'r2', cls=LinuxRouter, ip='192.168.1.2/24' )


	intfs = {'r2-eth0': {'ipAddrs': ['10.0.1.2/24'], 'mac': '00:88:00:00:00:02'},
                 'r2-eth1': {'ipAddrs': ['192.168.2.0/24']}}

	r2 = self.addHost('r2', cls=LinuxRouter,
                            intfDict=intfs,
                            quaggaConfFile='./quagga2.conf',
                            zebraConfFile='./zebra.conf')	

        s1 = self.addSwitch ('s1')

	self.addLink ( s1, r1)
	self.addLink ( s1, r2)
	        
	#self.addLink( s1, r1, intfName2='r1-eth1', params2={ 'ip' : '10.1.1.1/24' } )
	#self.addLink( s1, r2, intfName2='r2-eth1', params2={ 'ip' : '10.1.1.2/24' } ) 
        
	#self.addLink( s2, r1, intfName2='r1-eth2', params2={ 'ip' : '172.16.0.1/12' } )
        #self.addLink( s3, r1, intfName2='r1-eth3', params2={ 'ip' : '10.0.0.1/8' } )
        #self.addLink( s4, r1, intfName2='r1-eth4', params2={ 'ip' : '5.5.5.1/16' } )

        #h1 = self.addHost( 'h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
        #h2 = self.addHost( 'h2', ip='172.16.0.100/12', defaultRoute='via 172.16.0.1' )
        #h3 = self.addHost( 'h3', ip='10.0.0.100/8', defaultRoute='via 10.0.0.1' )
        #r2 = self.addNode( 'r2',cls=LinuxRouter, ip='5.5.5.100/16' )

        #self.addLink(r1,r2)


topos = { 'NetworkTopo' : NetworkTopo }

if __name__ == '__main__':

    setLogLevel('debug')
    topo = NetworkTopo()

    net = Mininet(topo=topo)

    net.start()

    CLI(net)

    net.stop()

    info("done\n")

