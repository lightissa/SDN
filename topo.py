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
    

   
    def __init__( self ):
    
        Topo.__init__(self)
        router = self.addNode( 'r0', cls=LinuxRouter, ip='194.12.230.1/24')

        " 1er sous-reseau"
        h1 = self.addHost( 'h1', ip='194.12.230.2/26',
                           defaultRoute='via 194.12.230.1' )
        h2 = self.addHost('h2', ip='194.12.230.3/26',
                           defaultRoute='via 194.12.230.1' )
          
        " 2em sous-reseau"
        h3 = self.addHost( 'h3', ip='194.12.230.66/26',
                           defaultRoute='via 194.12.230.65' )
        h4 = self.addHost( 'h4', ip='194.12.230.67/26',
                           defaultRoute='via 194.12.230.65' )
        """h5 = self.addHost( 'h5', ip='194.12.230.68/26',
                           defaultRoute='via 194.12.230.65' ) """

        " 3em sous-reseau"
        h6 = self.addHost( 'h6', ip='194.12.230.130/26',
                           defaultRoute='via 194.12.230.129' )
        h7 = self.addHost( 'h7', ip='194.12.230.131/26',
                           defaultRoute='via 194.12.230.129' )
        """   h8 = self.addHost( 'h8', ip='194.12.230.132/26',
                           defaultRoute='via 194.12.230.129' )
        h9 = self.addHost( 'h9', ip='194.12.230.133/26',
                           defaultRoute='via 194.12.230.129' ) """

        

        s1  =  self.addSwitch(  's1'  )
        s2  =  self.addSwitch(  's2'  )
        s3  =  self.addSwitch(  's3'  )
        self.addLink( router, s1, intfName1='r0-eth1',
                      params1={ 'ip' : '194.12.230.1/26' } )
        self.addLink( router,s2, intfName1='r0-eth2',
                      params1={ 'ip' : '194.12.230.65/26' } )
        self.addLink(  router, s3,intfName1='r0-eth3',
                      params1={ 'ip' : '194.12.230.129/26' } )
        self.addLink(h1,s1)
        self.addLink(h2,s1)  
        self.addLink(h3,s2)
        self.addLink(h4,s2)
        # self.addLink(h5,s2)
        self.addLink(h6,s3)
        self.addLink(h7,s3)
        #self.addLink(h8,s3)
        #self.addLink(h9,s3)
        
topos = { 'custom': ( lambda: NetworkTopo() ) }
