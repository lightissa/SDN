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
        router0= self.addNode( 'r0', cls=LinuxRouter, ip='194.12.230.1/24')
        router1= self.addNode( 'r1', cls=LinuxRouter, ip='11.0.0.1/8') 
        router2= self.addNode('r2', cls=LinuxRouter, ip='172.10.0.1/16')
        "hosts"
        h1 = self.addHost( 'h1', ip='194.12.230.2/24',
                           defaultRoute='via 194.12.230.1')
        h2 = self.addHost( 'h2', ip='194.12.230.3/24',
                           defaultRoute='via 194.12.230.1')
        h3 = self.addHost('h3', ip='172.10.0.2/16',
                           defaultRoute='via 172.10.0.1' )
        h4 = self.addHost( 'h4', ip='172.10.0.3/16',
                           defaultRoute='via 172.10.0.1' )
        "links"
        s1  =  self.addSwitch(  's1'  )
        s2  =  self.addSwitch(  's2'  )
        s3  =  self.addSwitch(  's3'  )
        s4 =   self.addSwitch(  's4'  )
        self.addLink(h1,s1)
        self.addLink(h2,s1)
        self.addLink(h3,s2)
        self.addLink(h4,s2)
        self.addLink(s1, router0,intfName2='r0-eth1',
                     params2={'ip' :'194.12.230.1/24'})
        self.addLink(s2, router1, intfName2='r2-eth1',
                     params2={'ip' :'172.10.0.3/16'})
        self.addLink(s4, router1, intfName2='r1-eth1',
                     params2={'ip' :'11.0.0.1/8'})
        self.addLink(s3, router0, intfName2='r0-eth2',
                     params2={'ip' :'10.0.0.2/8'})
        self.addLink(s4, router2, intfName2='r2-eth2',
                     params2={'ip' :'10.0.0.3/8'})
        self.addLink(s4, router1, intfName2='r1-eth2',
                     params2={'ip' :'10.0.0.1/8'})
        
        
topos = { 'custom': ( lambda: NetworkTopo() ) }
        

