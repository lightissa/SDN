from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    

    def build( self, **_opts ):
        router0 = self.addNode( 'r0', cls=LinuxRouter, ip='33.33.20.2/24')
        router1= self.addNode( 'r1', cls=LinuxRouter, ip='33.33.14.1/24') 
        router2= self.addNode('r2', cls=LinuxRouter, ip='33.33.20.1/24')
        router3= self.addNode('r3', cls=LinuxRouter, ip='33.33.34.1/24')
        router4= self.addNode('r4', cls=LinuxRouter, ip='33.33.14.2/24')

        """h1 = self.addHost( 'h1', ip='194.12.230.2/24',
                           defaultRoute='via 194.12.230.1' )
        h2 = self.addHost( 'h2', ip='194.12.230.3/24',
                           defaultRoute='via 194.12.230.1' )
        h3 = self.addHost('h3', ip='172.10.0.2/16',
                           defaultRoute='via 172.10.0.1' )
        h4 = self.addHost( 'h4', ip='172.10.0.3/16',
                           defaultRoute='via 172.10.0.1' )
        h5 = self.addHost( 'h5', ip='10.0.0.2/8',
                           defaultRoute='via 10.0.0.1' )
        h6 = self.addHost( 'h6', ip='10.0.0.3/8',
                           defaultRoute='via 10.0.0.1' )

        s1  =  self.addSwitch(  's1'  )
        s2  =  self.addSwitch(  's2'  )
        s3  =  self.addSwitch(  's3'  )"""

        self.addLink(router0, router2, intfName1='r0-eth1',intfName2='r2-eth1',
             params1={'ip' : '33.33.20.2/24'}, params2={'ip' :'33.33.20.1/24'})
        self.addLink(router2, router1, intfName1='r2-eth2',intfName2='r1-eth1',
             params1={'ip' : '33.33.12.2/24'}, params2={'ip' :'33.33.12.1/24'})
        self.addLink(router1, router4, intfName1='r1-eth2',intfName2='r4-eth1',
             params1={'ip' : '33.33.14.1/24'}, params2={'ip' :'33.33.14.2/24'})
        self.addLink(router4, router3, intfName1='r4-eth2',intfName2='r3-eth1',
             params1={'ip' : '33.33.34.2/24'}, params2={'ip' :'33.33.34.1/24'})
        self.addLink(router3, router0, intfName1='r3-eth2',intfName2='r0-eth2',
             params1={'ip' : '33.33.30.1/24'}, params2={'ip' :'33.33.30.2/24'})
        
topos = { 'custom': ( lambda: NetworkTopo() ) }
        
        


